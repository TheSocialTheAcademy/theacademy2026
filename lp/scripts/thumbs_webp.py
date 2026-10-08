# gen_thumbs.js が切り出した PNG を webp にして lp/assets/thumbs に置く
import os, json, tempfile
from PIL import Image
J = json.load(open(os.path.join(tempfile.gettempdir(), 'ta_thumbs.json')))
for s in J['slugs']:
    Image.open(os.path.join(tempfile.gettempdir(), f'ta_thumb_{s}.png')).convert('RGB').save(os.path.join(J['dir'], f'{s}.webp'), quality=88, method=6)
print('ok webp', len(J['slugs']), J['dir'])
