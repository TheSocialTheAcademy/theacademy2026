# gen_thumbs.js が切り出した PNG を webp にして lp/assets/thumbs に置く
import os, json, tempfile
from PIL import Image
J = json.load(open(os.environ.get('TA_JOB') or os.path.join(tempfile.gettempdir(), 'ta_thumbs.json')))  # TA_JOB で別の書き出しにも使う
for s in J['slugs']:
    Image.open(os.path.join(tempfile.gettempdir(), f"{J.get('prefix', 'ta_thumb_')}{s}.png")).convert('RGB').save(os.path.join(J['dir'], f'{s}.webp'), quality=88, method=6)
print('ok webp', len(J['slugs']), J['dir'])
