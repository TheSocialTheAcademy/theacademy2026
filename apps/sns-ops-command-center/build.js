#!/usr/bin/env node
/**
 * 分割版（sns-strategy-app/）から配布用の単一HTMLを再生成する。
 *
 *   node build.js
 *
 * 生成物:
 *   ./sns-ops-command-center-single.html
 *   ./sns-ops-command-center-single-fixed.html
 *
 * 注意: ユーザーは ~/Downloads/sns-ops-command-center-single.html を開いているため、
 *       --sync を付けるとそちらにも同時にコピーする。
 */
const fs = require("fs");
const path = require("path");
const os = require("os");

const SRC = path.join(__dirname, "sns-strategy-app");
const read = (name) => fs.readFileSync(path.join(SRC, name), "utf8");

const html = `<!doctype html>
<html lang="ja">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>SNS Ops Command Center</title>
    <style>
${read("styles.css")}
    </style>
  </head>
  <body>
    <div id="app"></div>
    <script>
${read("data.js")}
    </script>
    <script>
${read("social-icons.js")}
    </script>
    <script>
${read("app.js")}
    </script>
  </body>
</html>
`;

const targets = [
  path.join(__dirname, "sns-ops-command-center-single.html"),
  path.join(__dirname, "sns-ops-command-center-single-fixed.html"),
  path.join(__dirname, "dist", "index.html"),
];

if (process.argv.includes("--sync")) {
  const downloads = path.join(os.homedir(), "Downloads");
  targets.push(
    path.join(downloads, "sns-ops-command-center-single.html"),
    path.join(downloads, "sns-ops-command-center-single-fixed.html")
  );
}

targets.forEach((file) => {
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, html);
  console.log(`built: ${file}`);
});

console.log(`\n${targets.length} file(s) written. ${process.argv.includes("--sync") ? "" : "\nヒント: --sync を付けると ~/Downloads 直下（ユーザーが開いているファイル）にも同期します。"}`);
