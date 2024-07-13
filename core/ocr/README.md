# Распознавание текста на видео

## Documentation
* [Installation guide](#installation-guide)
* [Apply](#apply)
* [Todo](#TODO)
* [Speed test](#speed-test)
* [Llama 3 8B post processing test](#llama-3-8b-post-processing-test)
* [Useful links](#useful-links)

# Installation guide
1. Pip packages - `pip install -r requirement.txt`
2. If OS Ubuntu/Linux - `sh setup_environment/download_opencv_for_ubuntu.sh`
3. Download llama and llava - `sh setup_environment/download_ollama_with_models_linux.sh`
4. Setup easyocr, add `test` to args if needed videos - `python3 setup_env.py`

# Apply
1. Пример применения - `how_to_apply_main_video_to_text.py`
2. Main файл модуля - `main_video_to_text.py`

## TODO
1. [X] Собрать чистый код с Easy OCR.
2. [X] Сделать минимальную пост обработку текста. Для фильтрации плохо распознанных символов.
3. [X] Оптимизировать по ресурсам. Multiprocessing/multithreading. Ram preload. Photo preproc. EasyOCR model settings for speed up.
4. [X] Опционально. Поднять небольшую llm для пост обработки текста.
5. [X] Дописать промпт.
6. [X] Собрать код.
7. [X] Запустить скоринг видосов.

## Speed test
### Default settings
1. GPU
  - 1 video, 10 frames with saving frames - ~8-10 seconds
  - 1 video, 10 frames without saving frames - ~7-10 seconds
  - 1 video, 15 frames without saving frames - ~11-13 seconds
  - 1 video, 15 frames without saving frames, with model post proc - ~26-33 seconds
  - Init reader (load models in memory, etc.) - 2-3 seconds
  - Detect and recognize text on 10 frames - 3-7 seconds
  - Detect and recognize text on 15 frames - 3-10 seconds
2. CPU
  - 1 video, 10 frames with saving frames - ~27 seconds
  - 1 video, 10 frames without saving frames - ~25 seconds
  - 1 video, 15 frames without saving frames - ~42-45 seconds

## Llama 3 8B post processing test
1. videos/35_3a_021d5db24560a64cc00b79d97a4a_fhd.mp4

Input:
```
{0: 'Мам, можно мне набор К-9 Vidar?',
 34: 'Мам, можно мне набор К-9 Vidar?',
 69: 'Мам, можно мне набор К-9 Vidar?',
 104: 'Мам, можно мне набор К-9 Vidar? Нет; сын У нас уже есть К-9 дома',
 139: 'Мам, можно мне набор К-9 Vidar? Нет; сын нас уже есть К-9 дома',
 173: 'Мам, можно мне набор К-9 Vidar? Нет; сын нас уже есть К-9 дома',
 208: 'Мам, можно мне набор К-9 Vidar? Нет; сын нас уже есть К-9 дома ~г = - '
      '₽  ',
 243: '',
 278: '',
 313: 'К-9 дома:',
 347: 'К-9 дома: : 7086 100',
 382: 'К-9 дома: j 3 7086 10',
 417: 'К-9 дома: 7086',
 452: 'К-9 дома: 7086',
 487: 'К-9 дома: 1002 086'}
```
Output:
```
('мам, можно мне набор к-9 vidar? нет; сын у нас уже есть к-9 дома. г - к-9 '
 'дома: 7086 100 к-9 дома: j 3 7086 10 к-9 дома: 7086')
```

2. videos/ed_db_4c8de8474648be7639b3627cabf3_fhd.mp4

Input:
```
{0: 'dWl? #AFLEISCHACHSE SHAKAL',
 80: '',
 161: 'SHAKAL НАКСШМЕ',
 242: "'sH [LESCHACI",
 323: 'FLEISCHAGHSE [ULEL] Salaleaver BALL ChAsER shakal 11E БПшч',
 404: 'EEUFEQ Bt [ULEG] Sululeaver EALL CHFSER shakal 116 БПы',
 485: 'ШънukоY шана Iai',
 566: 'аg99#',
 647: '@gguWll [ecul',
 728: 'LOLEAVER CUREL MIXASTIK SUFSRRSK NSPECIURBOLS',
 809: 'SKIFF-',
 890: 'SKIFF-',
 971: 'SKYL',
 1052: 'GEUFEE [AIM] Skiff CROSSBAR HERO 1я; 57 каН'}
```
Output:
```
''
```

3. videos/94_3d_ea40da9645acacf006df16b9bb75_fhd.mp4

Input:
```
{0: 'MB M BEAUTY COSMETICS ПОСТАКНЕ',
 22: 'MB M BEAUTY COSMETICS ПОСТАКНЕ',
 45: 'MB M BEAUTY COSMETICS ПОСТАКНЕ',
 68: 'MB M BEAUTY COSMETICS ПОСТАКНЕ',
 91: 'NB M BEAUTY COSAIILTNICS \'uecr & MyCli Jiso "еаj Prol Pucl [pldetml '
     "ТЫПvqиz Fcuл; #4о arcruiur нa' ПИЛИНГ ДЛЯ ЛИЦА МуCli Soft Peel Epidermal "
     'Revitalizing Comlpex МуСli Prof | Peel МуCli Pecling € Rinnоv Epidermico '
     'wamento Prof Pecl Icoцo DECCLLEIE Epidermal сткniiо Renovating Prcling # '
     "'bEcoutrtt ииDnc",
 113: 'MB M BEAUTY COSMETICS СУХОСТЬ ИШЕЛУШЕНИЕ',
 136: 'MB M BEAUTY COSMETICS СУХОСТЬ И ШЕЛУШЕНИЕ',
 159: 'MB M BEAUTY COSMETICS СУХОСТЬ И ШЕЛУШЕНИЕ',
 182: 'MB M BEAUTY COSMETMCS СЫВОРОТКА SKIN & LAB Barrierderm Millky Serum '
      'TAfR ERDERN| "Lk?   "SERUM] [уче ₽ЫПЧя и5гu \'SKIN & \' LAB BARRIERDI '
      "#XY , }ЕRM 'ERUWN",
 205: 'MB M BEAUTY COSMETMCS СЫВОРОТКА SKIN & LAB Barrierderm Millky Serum '
      'TAfR ERDERN| "Lk?   "SERUM Дуча ₽ЫПЕд Tсmл \'SKIN & \'LAB BAFRIERDI #JY '
      'IERM SERUN',
 227: 'MB M BEAUTY COSMETICS МОРЩИНКИ ВОКРУГ ГЛАЗ',
 250: 'MB M BEAUTY COSMETICS МОРЩИНКИ ВОКРУГ ГЛАЗ',
 273: 'MB M BEAUTY COSMETICS МОРЩИНКИ ВОКРУГ ГЛАЗ',
 296: 'MB BLAUTY COзEMCS 5* c CEM; Ga KPEM ВОКРУГ ГЛАЗ EУECELL Еye Contour '
      'Cream 8 Ii 8 8 € 2 #cc лошту { [ CEN 1 8 1 GEN',
 319: ''}
```
Output:
```
('mb m beauty cosmetics - постакне. nb m beauty cosmetics - postakne. муcli '
 'soft peel epidermal revitalizing complex. мусli prof peel. муcli pecling. '
 'rinnov epidermico wamento prof pecl icoцo decclleie epidermal сткнiiо '
 'renovating prcling. mb m beauty cosmetics - сушость ишелушение. skin lab '
 'barrierderm millky serum tafr erdern lk? serum. mb m beauty cosmetics - '
 'сыворотка. skin lab barrierderm millky serum tafr erdern lk? serum. mb m '
 'beauty cosmetics - морщинки вокруг глаз. eуecell eye contour cream.')
```

4. videos/03_eb_47329b1943349255453b6cec625d_fhd.mp4

Input:
```
{0: 'FUNv Этуарь ТВОЯ КОЖКА СКАЭКЕТ TFEIF СПАСИБО',
 63: "'Этуас Ь ПАРФЮМЕРИЯ КОСМЕТИКА АКСЕССУАРЫ ТВОЯ КОЖКА СКАЖКЕТ TEБIE "
     'СпАСИЕК',
 126: "'ЭтуаОь ПАРФЮНЕРИЯ КОСМЕТИКА AKULGGУAPЫ ТВОЯ КОЖКА СКАЭКЕТ TЕБE: "
      'СпАСИЕК',
 189: 'лlyar Фь ПАРФЮМЕРИЯ КОСМЕТИКА АКСЕССУАРЫ HANEL Dlor ППодписывайся Dlor',
 252: 'CHANEL Dior Dior Dlor [одписывайся SulonAun ДиатАнЦиюю Dloз оыПииленую '
      'wNaиan',
 316: 'Dior Dior Dior Dlor [одписывайся ом4г ~аиоu$ NF саьакиъе оууизоз Ааиию',
 379: 'WIvI Dior Dior hlukotul Dior GlI flhh WNUJI 40%0 4U Gl%',
 442: 'Dior Dior Dior DIOROUGE Dior 50% IП2 40%6 40% 5U% АистАнчи 15 Метьд',
 505: 'Dior Sl%h DIOROUGE Dior 40% 40% il%b',
 568: 'Juhbe] каg Увлажнение Blore Biore Biore 2 +у"7 "#EЛ Ж] oltl (labl)u '
      'Lэz) 741ъж #JfJ ^ +4х+1= FActs] Wan Nohgufe',
 632: '907 9 као Увлажнение [Ellleзъ [Wlsflile Ээкокоо Biore Biore  5a Biore '
      "7+уV7 # Еf Ж] vett' Blebl) | Lэz) 75 8 5* t JеЛЛ ^ д1zэ+- Fihl { aash "
      'Volitute',
 695: '1, ue) F #h E# Faclal Caic Для Склонной K акне DzW 12 Biore Z #утл ЖёН '
      "Ж =tE =+tzlt FАt  НЗБ #Еа 7эъ лёЮIЕ 7эх4т 'Wash Ache",
 758: '*> e ) Gleb 2# Аvi K ВХКA увлажнение шталый пля умыпания; тоЛЬ Biore '
      "СМЯгЧающий | 1кожу Зiore 2+> нын Biore 'эгэ' [x 3э5 ne тэbэtстo n uвns "
      'DrJv Зкера 12 1a Biore 7+ут7 #ЕН Я (@8ElH Lal) ъэъъ01F~ 77 < "уз#Е3++ '
      'Yiaawaч Moktue',
 821: '"373 сэгаzч 7ы; тарп аэ-7 1e 25  ЕХDRA увлажнение p Biore 1 -25  749, 7 '
      '#у" 7 #[3Ж х5эё0t1 ` #lli t ТХтХФзЮ^  Тэву 4v 4{atn-J #ы woyh 0JContal '
      'каб;',
 885: "Ут'_ We) cvа  7 Контроль себума (aun #Rbbtiъ Rt}э #m@тlV v 1 Biore Z+v' "
      '#tEn M] ху ~эщ0tt y gflz: хтходы ~ =.ata- - натаs cсь -'}
```
Output:
```
''
```

5. videos/8c_58_96608b7a4834883ea2dd1c884c63_fhd.mp4

Input:
```
{0: '',
 80: 'нигАе ещёне пижофе вкуснее; 4a и такими видами ещё =',
 160: '',
 240: 'Старбакстут ссамым красивым виДом на море и скамы:',
 320: '',
 401: '',
 481: '',
 561: ')Анако; Вы можете купить кофе B соседнем магазине за 4ОP и поАнятьсЯ в '
      'заброшенное зАание; насАажАаться закатом:',
 641: 'Анако; Вы можете купить кофе B соседнем магазине за 4ОP и поАнятЬсЯ '
      'заброшенное зАание; насАажАаться закатом:',
 721: '',
 802: 'Приезжайте B БЕЙРУТ',
 882: '',
 962: '',
 1042: '₽',
 1123: ''}
```
Output:
```
('нигде еще не пишется вкуснее; старбукстут с самым красивым видом на море и '
 'скалами. вы можете купить кофе в соседнем магазине за 40 рублей и понять '
 'себя в заброшенном заросшем месте, насаждаясь закатом: приезжайте в бейрут.')
```

6. videos/bf_ee_85fb6b80491db79e8baebe5c9d80_fhd.mp4

Input:
```
{0: 'Экспресс-чисuка кроссовок Sune Step ш',
 36: 'Экcпресс-чистка Кроссовок',
 73: 'Экcmpесс-чисuкa Кроссовок',
 109: 'ЭкcmpесG-чисuкa Кросс@B@к',
 146: 'ЭкcmeсG чиGuка Кр@Gс@BоK',
 182: 'ЭкспрeсGчиGuка кросс@вок',
 219: 'ЭкcmeсGчиGuа Кроссовок',
 255: 'Экспресс-чистка кроссовок',
 292: 'Сохрани и поделись GJ друзьями; если [олезно Мом',
 328: '@охрани и поделись & {рузьями если полезно',
 365: '@охрани и Поделись & {рузьями если полезно',
 401: 'Сохрани и поделись & {рузьями; если полезно',
 438: 'Сохрани и поделись & {рузьями; если полезно',
 474: 'Для "РO(COЗOM 100 mL Сохрани и поделись c друзьями, если полезно Supe '
      'Step шиилэны',
 511: 'шиmньлля ШО(ОВO7 129 ml Сохрани и поделись c друзьями, если полезно '
      'SSupe Step'}
```
Output:
```
('экспресс-чистка кроссовок sune step. сохрани и поделись с друзьями; если '
 'полезно. для рекомендации 100 ml. сохрани и поделись с друзьями, если '
 'полезно.')
```

7. videos/5d_b1_33afba83485ab7bb5dcc1cfe0c90_fhd.mp4

Input:
```
{0: 'Это не Может так продолжаться!',
 86: 'кim M A N I[ Больше не буду; клянусь',
 173: 'й I, 0 Di=ш 4 =',
 259: 'K IN 0 . М я NI ₽ Что?!',
 346: 'к ШI " цие Мне больно!',
 432: 'кI 9 шарi Что c тобой?',
 519: '# I = 0 и АN I A',
 605: '#I . Ш Д Кi A',
 692: '#I: 0 FL A ШI A',
 778: 'KIl 0 . М А NI A',
 865: 'к , 9 N n !д',
 951: '4 =ш ш } _El',
 1038: '',
 1124: ''}
```
Output:
```
('это не может так продолжаться! каким образом mani больше не будет; я '
 'клянусь, что это не может быть. что?! мне больно! что с тобой? я не понимаю '
 'и не хочу ничего делать. шахматная игра кончена. моя жизнь не моя. кто-то '
 'другой управляет мной. я не хочу больше играть в эту игру.')
```

## Useful links
- [Ollama CLI doc](https://github.com/ollama/ollama/blob/main/docs/api.md#generate-embeddings)
- [Ollama docker hub](https://hub.docker.com/r/ollama/ollama)
- [Ollama docker guide](https://github.com/ollama/ollama/blob/main/docs/docker.md)
- [EasyORC doc](https://www.jaided.ai/easyocr/documentation/)
- [Llama-3-8b Hugging Face](https://huggingface.co/meta-llama/Meta-Llama-3-8B)
- [License Llama 3 8B (можно коммерческое использование)](https://huggingface.co/meta-llama/Meta-Llama-3-8B/blob/main/LICENSE)
- [License EasyOCR (можно коммерческое использование)](https://github.com/JaidedAI/EasyOCR/blob/master/LICENSE)

