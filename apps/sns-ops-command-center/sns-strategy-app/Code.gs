/**
 * SNS Ops Command Center - チーム共有用 Apps Script
 *
 * このコードは、Googleスプレッドシートに紐づく「コンテナバインドスクリプト」として使います。
 * 使い方は同封の SETUP_GUIDE.md を参照してください。
 *
 * 仕組み:
 * - シート「state」のA1セルに、アプリの全データをJSON文字列として1つだけ保存します
 * - B1セルには最終更新日時（ISO文字列）を保存します
 * - doGet(): 現在のデータを返す（アプリが数秒おきに呼び出します）
 * - doPost(): 新しいデータを保存する（アプリが編集のたびに呼び出します）
 * - 簡易的な競合検知つき: 自分が最後に取得した時刻と、シートの現在の更新時刻が
 *   ズレている場合は上書きせず、シート側の最新データを返します
 *   （＝他の人が自分より後に保存していたら、自分の変更は失われず、警告つきで
 *   最新データに置き換わります。もう一度編集し直してください）
 */

const SHEET_NAME = 'state';

function doGet(e) {
  const sheet = getSheet_();
  const json = sheet.getRange('A1').getValue() || '{}';
  const updatedAt = sheet.getRange('B1').getValue() || '';
  return jsonResponse_({ state: safeParseJson_(json), updatedAt: String(updatedAt) });
}

function doPost(e) {
  const sheet = getSheet_();
  let body;
  try {
    body = JSON.parse(e.postData.contents);
  } catch (err) {
    return jsonResponse_({ error: 'invalid_json' });
  }

  const currentUpdatedAt = String(sheet.getRange('B1').getValue() || '');

  // 競合チェック: サーバーに既にデータがあり(currentUpdatedAtが存在)、
  // クライアントが最後に取得したupdatedAtと一致しない場合は上書きしない。
  // baseUpdatedAtが空文字(＝クライアントが一度もデータを取得していない)場合も、
  // サーバーに既存データがあれば競合として扱う。
  if (currentUpdatedAt && body.baseUpdatedAt !== currentUpdatedAt) {
    const currentJson = sheet.getRange('A1').getValue() || '{}';
    return jsonResponse_({
      conflict: true,
      state: safeParseJson_(currentJson),
      updatedAt: currentUpdatedAt,
    });
  }

  const now = new Date().toISOString();
  sheet.getRange('A1').setValue(JSON.stringify(body.state || {}));
  sheet.getRange('B1').setValue(now);
  return jsonResponse_({ ok: true, updatedAt: now });
}

function getSheet_() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let sheet = ss.getSheetByName(SHEET_NAME);
  if (!sheet) {
    sheet = ss.insertSheet(SHEET_NAME);
    sheet.getRange('A1').setValue('{}');
    sheet.getRange('B1').setValue(new Date().toISOString());
    sheet.getRange('A2').setValue('↑ A1に全データがJSON形式で入っています。手動で編集しないでください。');
  }
  return sheet;
}

function safeParseJson_(text) {
  try {
    return JSON.parse(text);
  } catch (err) {
    return {};
  }
}

function jsonResponse_(obj) {
  return ContentService
    .createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}
