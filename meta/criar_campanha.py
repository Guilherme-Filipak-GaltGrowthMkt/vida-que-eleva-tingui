"""Cria a campanha da Semana Especial Vida que Eleva na conta CA01 - IASD Tingui.

Tudo é criado PAUSADO. Uso: python3 meta/criar_campanha.py  (lê o token do .env do projeto Casais)
Grava os IDs criados em meta/ids.json.
"""
import json, os, subprocess, sys, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV = os.path.join(os.path.dirname(ROOT), 'Casais', '.env')
if not os.path.exists(ENV):  # antes da pasta Casais ir para dentro de "IASD Tingui"
    ENV = os.path.join(os.path.dirname(os.path.dirname(ROOT)), 'Casais', '.env')
env = dict(l.strip().split('=', 1) for l in open(ENV) if '=' in l and not l.startswith('#'))
TOKEN, ACT = env['META_TOKEN'], env['META_AD_ACCOUNT']
PAGE, IG, PIXEL = env['META_PAGE_ID'], env['META_IG_ID'], env['META_PIXEL_ID']
V = 'v23.0'
LINK = 'https://guilherme-filipak-galtgrowthmkt.github.io/vida-que-eleva-tingui/'
REMARKETING = '120241920908470707'  # [SITE] [TODOS] - 30D
START = '2026-11-07T00:00:00-0300'
DAILY = 6667  # R$ 66,67/dia: R$ 300 ÷ 4,5 dias (sáb 07/11 00h → qua 11/11 12h)

IDS_FILE = os.path.join(ROOT, 'meta', 'ids.json')
ids = json.load(open(IDS_FILE)) if os.path.exists(IDS_FILE) else {}
def save(): json.dump(ids, open(IDS_FILE, 'w'), indent=1, ensure_ascii=False)

def call(path, method='POST', files=None, host='graph.facebook.com', **params):
    cmd = ['curl', '-s', '-X', method, f'https://{host}/{V}/{path}', '-F', f'access_token={TOKEN}']
    for k, v in params.items():
        cmd += ['-F', f'{k}={json.dumps(v, ensure_ascii=False) if isinstance(v, (dict, list)) else v}']
    for k, f in (files or {}).items():
        cmd += ['-F', f'{k}=@{f}']
    r = json.loads(subprocess.run(cmd, capture_output=True, text=True).stdout)
    if 'error' in r:
        sys.exit(f'ERRO em {path}: {json.dumps(r["error"], ensure_ascii=False)}')
    return r

def get(path, **params):
    q = '&'.join(f'{k}={v}' for k, v in params.items())
    out = subprocess.run(['curl', '-s', f'https://graph.facebook.com/{V}/{path}?{q}&access_token={TOKEN}'],
                         capture_output=True, text=True).stdout
    return json.loads(out)

GEO = {'custom_locations': [{'latitude': -25.3851905, 'longitude': -49.2285629, 'radius': 2,
                             'distance_unit': 'kilometer', 'country': 'BR'}],
       'location_types': ['home', 'recent']}

LOCAL = ('🗓 Quarta a sexta às 20h · Sábado a partir das 9h15\n'
         '📍 Igreja Adventista Tingui · Rua Guilherme Ihlenfeldt, 778')

ADS = [
    {'key': 'AD01', 'video': 'v1', 'adset': 'aberto', 'content': 'video-v1-moradores',
     'title': 'Vida que Eleva · 11 a 14/11 · Gratuito',
     'text': ('Você que mora no Bacacheri ou no Tingui: temos um convite especial para você. 💛\n\n'
              'De 11 a 14 de novembro, a Semana Especial Vida que Eleva traz quatro encontros com reflexões '
              'bíblicas sobre fé, escolhas e recomeços, com o Pr. Gilmar.\n\n' + LOCAL + '\n\n'
              'É gratuito. Venha você, sua família, e a vontade de respirar um pouco. '
              'Faça sua inscrição e receba todas as informações.')},
    {'key': 'AD02', 'video': 'v2', 'adset': 'aberto', 'content': 'video-v2-nao-desiste',
     'title': 'Uma semana para olhar a vida com esperança',
     'text': ('O brasileiro tem uma coisa que ninguém tira: a gente não desiste. Mesmo quando o dia vai mal '
              'e o ambiente está pesado, a gente sorri e segue.\n\n'
              'Essa esperança merece ser cuidada. 💛\n\n'
              'Por isso, a Igreja Adventista do Tingui convida você para a Semana Especial Vida que Eleva: '
              'quatro encontros gratuitos com reflexões bíblicas sobre fé, escolhas e recomeços.\n\n'
              + LOCAL + '\n\nFaça sua inscrição gratuita.')},
    {'key': 'AD03', 'video': 'v4', 'adset': 'aberto', 'content': 'video-v4-cansado',
     'title': 'Você anda cansado? Venha respirar',
     'text': ('A semana passa rápido, né? O trabalho e os afazeres tomam conta do dia, e o cansaço só aumenta.\n\n'
              'Temos um convite para você: de 11 a 14 de novembro, quatro encontros gratuitos com reflexões '
              'bíblicas sobre fé, escolhas e recomeço. 💛\n\n' + LOCAL + '\n\n'
              'Faça sua inscrição e receba todas as informações.')},
    {'key': 'AD04', 'video': 'v3', 'adset': 'remarketing', 'content': 'video-v3-remarketing',
     'title': 'Ainda dá tempo de se inscrever',
     'text': ('Você já viu o nosso convite, mas ainda não fez sua inscrição na Semana Especial Vida que Eleva. 💛\n\n'
              'São quatro encontros gratuitos, de 11 a 14 de novembro, com reflexões sobre fé, escolhas e, quem sabe, '
              'um recomeço.\n\n' + LOCAL + '\n\n'
              'A inscrição leva menos de 1 minuto. Te esperamos!')},
]

# 1. Vídeos
for v in sorted({a['video'] for a in ADS}):
    if f'video_{v}' in ids: continue
    print('enviando', v, flush=True)
    r = call(f'{ACT}/advideos', host='graph-video.facebook.com', name=f'Vida que Eleva {v}',
             files={'source': os.path.join(ROOT, 'criativos', f'{v}.MOV')})
    ids[f'video_{v}'] = r['id']; save()

# espera processar e pega a capa
for v in sorted({a['video'] for a in ADS}):
    if f'thumb_{v}' in ids: continue
    for _ in range(60):
        r = get(ids[f'video_{v}'], fields='status,thumbnails{uri,is_preferred}')
        th = r.get('thumbnails', {}).get('data', [])
        if r.get('status', {}).get('video_status') == 'ready' and th:
            ids[f'thumb_{v}'] = next((t['uri'] for t in th if t.get('is_preferred')), th[0]['uri']); save()
            break
        time.sleep(10)
    else:
        sys.exit(f'vídeo {v} não terminou de processar; rode de novo daqui a pouco')

# 2. Campanha (CBO)
if 'campaign' not in ids:
    ids['campaign'] = call(f'{ACT}/campaigns', name='[LEADS] Vida que Eleva Tingui | 07-11/11',
                           objective='OUTCOME_LEADS', status='PAUSED', special_ad_categories=[],
                           daily_budget=DAILY, bid_strategy='LOWEST_COST_WITHOUT_CAP')['id']; save()

# 3. Conjuntos
ADSETS = {
    'aberto': ('Tingui 2km | 18+ | Adv+ Aberto',
               {'geo_locations': GEO, 'age_min': 18, 'age_max': 65,
                'targeting_automation': {'advantage_audience': 1}}),
    'remarketing': ('Tingui 2km | 18+ | Remarketing [SITE] 30D',
                    {'geo_locations': GEO, 'age_min': 18, 'age_max': 65,
                     'custom_audiences': [{'id': REMARKETING}],
                     'targeting_automation': {'advantage_audience': 0}}),
}
for k, (name, targeting) in ADSETS.items():
    if f'adset_{k}' in ids: continue
    ids[f'adset_{k}'] = call(f'{ACT}/adsets', name=name, campaign_id=ids['campaign'], status='PAUSED',
                             optimization_goal='OFFSITE_CONVERSIONS', billing_event='IMPRESSIONS',
                             destination_type='WEBSITE', start_time=START,
                             promoted_object={'pixel_id': PIXEL, 'custom_event_type': 'LEAD'},
                             targeting=targeting)['id']; save()

# 4. Criativos e anúncios
for a in ADS:
    if f'ad_{a["key"]}' in ids: continue
    spec = {'page_id': PAGE, 'instagram_user_id': IG,
            'video_data': {'video_id': ids[f'video_{a["video"]}'], 'image_url': ids[f'thumb_{a["video"]}'],
                           'message': a['text'], 'title': a['title'],
                           'call_to_action': {'type': 'SIGN_UP', 'value': {'link': LINK}}}}
    cr = call(f'{ACT}/adcreatives', name=f'{a["key"]} · {a["content"]}', object_story_spec=spec,
              url_tags=f'utm_source=meta&utm_medium=paid&utm_campaign=vida-que-eleva&utm_content={a["content"]}')
    ids[f'creative_{a["key"]}'] = cr['id']
    ids[f'ad_{a["key"]}'] = call(f'{ACT}/ads', name=f'{a["key"]} · {a["content"]}', adset_id=ids[f'adset_{a["adset"]}'],
                                 creative={'creative_id': cr['id']}, status='ACTIVE')['id']; save()
    print('anúncio', a['key'], 'ok', flush=True)

print(json.dumps(ids, indent=1))
