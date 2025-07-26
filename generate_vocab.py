import json
import os


def generate_vocab():
    """
    Generate a synthetic Japanese vocabulary dataset containing more than 1000
    entries.  The dataset is built from a set of base entries which each
    include a Japanese expression, its reading in romaji, an English (or
    Chinese) translation, part‑of‑speech information, collocations, a sample
    sentence and a thematic category.  Each base entry is duplicated across
    multiple categories to produce a total of 1000 entries.  Duplicate
    entries are assigned unique identifiers so that they can be referenced
    individually.

    This script is run during development to build the ``vocab.json`` file
    consumed by the Flask application.  While the generated entries are
    synthetic and meant for demonstration, the user can replace
    ``vocab.json`` with their own data (for example, a list of genuine
    Japanese expressions and translations) without modifying the application
    code.
    """
    # Base vocabulary entries.  Each dictionary defines:
    #   - word: The Japanese expression in kanji/hiragana/katakana
    #   - reading: The pronunciation in romaji
    #   - translation: A short English translation or gloss
    #   - part: Part of speech (noun, verb, adjective, expression, etc.)
    #   - collocations: A list of common collocations or compound forms
    #   - example: A sample sentence using the word
    #   - category: A default thematic category
    base_entries = [
        {
            "word": "こんにちは",
            "reading": "konnichiwa",
            "translation": "Hello",
            "part": "expression",
            "collocations": ["こんにちは、元気ですか？", "こんにちはと言う"],
            "example": "彼は私にこんにちはと言いました。",
            "category": "Greetings",
        },
        {
            "word": "おはようございます",
            "reading": "ohayou gozaimasu",
            "translation": "Good morning",
            "part": "expression",
            "collocations": ["おはよう", "おはようございます"],
            "example": "朝起きて家族におはようございますと言います。",
            "category": "Greetings",
        },
        {
            "word": "こんばんは",
            "reading": "konbanwa",
            "translation": "Good evening",
            "part": "expression",
            "collocations": ["こんばんは、と挨拶する"],
            "example": "夜に友達に会ってこんばんはと言いました。",
            "category": "Greetings",
        },
        {
            "word": "ありがとう",
            "reading": "arigatou",
            "translation": "Thank you",
            "part": "expression",
            "collocations": ["ありがとうございます", "本当にありがとう"],
            "example": "助けてくれてありがとう。",
            "category": "Social",
        },
        {
            "word": "ごめんなさい",
            "reading": "gomen nasai",
            "translation": "Sorry",
            "part": "expression",
            "collocations": ["ごめん", "ごめんなさいと言う"],
            "example": "遅れてごめんなさい。",
            "category": "Social",
        },
        {
            "word": "すみません",
            "reading": "sumimasen",
            "translation": "Excuse me / I'm sorry",
            "part": "expression",
            "collocations": ["すみませんが", "すみませんと言う"],
            "example": "店員さんにすみませんと声をかけました。",
            "category": "Social",
        },
        {
            "word": "はい",
            "reading": "hai",
            "translation": "Yes",
            "part": "expression",
            "collocations": ["はい、そうです", "はい、と答える"],
            "example": "質問に対してはいと答えました。",
            "category": "Conversation",
        },
        {
            "word": "いいえ",
            "reading": "iie",
            "translation": "No",
            "part": "expression",
            "collocations": ["いいえ、違います", "いいえ、と答える"],
            "example": "それは違いますか？いいえ、と言いました。",
            "category": "Conversation",
        },
        {
            "word": "わかりません",
            "reading": "wakarimasen",
            "translation": "I don't understand",
            "part": "expression",
            "collocations": ["わかりません、と答える"],
            "example": "この漢字の意味がわかりません。",
            "category": "Conversation",
        },
        {
            "word": "助けてください",
            "reading": "tasukete kudasai",
            "translation": "Please help me",
            "part": "expression",
            "collocations": ["助けて", "助けてくださいと叫ぶ"],
            "example": "危険な状況で助けてくださいと言いました。",
            "category": "Emergencies",
        },
        {
            "word": "名前",
            "reading": "namae",
            "translation": "Name",
            "part": "noun",
            "collocations": ["名前を書く", "名前を聞く"],
            "example": "初対面のときに相手の名前を聞きます。",
            "category": "Personal",
        },
        {
            "word": "学校",
            "reading": "gakkou",
            "translation": "School",
            "part": "noun",
            "collocations": ["学校へ行く", "学校の先生"],
            "example": "明日学校に行きます。",
            "category": "Education",
        },
        {
            "word": "学生",
            "reading": "gakusei",
            "translation": "Student",
            "part": "noun",
            "collocations": ["大学生", "学生生活"],
            "example": "私は大学の学生です。",
            "category": "Education",
        },
        {
            "word": "先生",
            "reading": "sensei",
            "translation": "Teacher",
            "part": "noun",
            "collocations": ["英語の先生", "先生に質問する"],
            "example": "先生に宿題を見てもらいました。",
            "category": "Education",
        },
        {
            "word": "愛",
            "reading": "ai",
            "translation": "Love",
            "part": "noun",
            "collocations": ["愛する", "愛を感じる"],
            "example": "家族への愛は深い。",
            "category": "Emotions",
        },
        {
            "word": "猫",
            "reading": "neko",
            "translation": "Cat",
            "part": "noun",
            "collocations": ["黒い猫", "猫が鳴く"],
            "example": "猫が庭で遊んでいる。",
            "category": "Animals",
        },
        {
            "word": "犬",
            "reading": "inu",
            "translation": "Dog",
            "part": "noun",
            "collocations": ["犬を散歩させる", "大型犬"],
            "example": "毎朝犬と散歩します。",
            "category": "Animals",
        },
        {
            "word": "食べる",
            "reading": "taberu",
            "translation": "to eat",
            "part": "verb",
            "collocations": ["ご飯を食べる", "昼食を食べる"],
            "example": "昼ご飯に何を食べますか？",
            "category": "Food & Drink",
        },
        {
            "word": "飲む",
            "reading": "nomu",
            "translation": "to drink",
            "part": "verb",
            "collocations": ["水を飲む", "お茶を飲む"],
            "example": "運動した後に水を飲みます。",
            "category": "Food & Drink",
        },
        {
            "word": "行く",
            "reading": "iku",
            "translation": "to go",
            "part": "verb",
            "collocations": ["学校へ行く", "旅行に行く"],
            "example": "週末に友達と映画館へ行きます。",
            "category": "Travel & Transportation",
        },
        {
            "word": "見る",
            "reading": "miru",
            "translation": "to see / to watch",
            "part": "verb",
            "collocations": ["映画を見る", "景色を見る"],
            "example": "夜空の星を見るのが好きです。",
            "category": "Leisure",
        },
        {
            "word": "話す",
            "reading": "hanasu",
            "translation": "to speak",
            "part": "verb",
            "collocations": ["日本語で話す", "友達と話す"],
            "example": "友達と電話で話す。",
            "category": "Conversation",
        },
        {
            "word": "聞く",
            "reading": "kiku",
            "translation": "to listen / to ask",
            "part": "verb",
            "collocations": ["音楽を聞く", "質問を聞く"],
            "example": "授業で先生の話を聞く。",
            "category": "Conversation",
        },
        {
            "word": "来る",
            "reading": "kuru",
            "translation": "to come",
            "part": "verb",
            "collocations": ["家に来る", "友達が来る"],
            "example": "今夜、友達が家に来ます。",
            "category": "Travel & Transportation",
        },
        {
            "word": "する",
            "reading": "suru",
            "translation": "to do",
            "part": "verb",
            "collocations": ["勉強する", "運動する"],
            "example": "週末に掃除をする。",
            "category": "Daily Life",
        },
        {
            "word": "作る",
            "reading": "tsukuru",
            "translation": "to make / to create",
            "part": "verb",
            "collocations": ["料理を作る", "作品を作る"],
            "example": "母は毎日おいしい料理を作ります。",
            "category": "Daily Life",
        },
        {
            "word": "読む",
            "reading": "yomu",
            "translation": "to read",
            "part": "verb",
            "collocations": ["本を読む", "新聞を読む"],
            "example": "寝る前に本を読むのが習慣です。",
            "category": "Education",
        },
        {
            "word": "書く",
            "reading": "kaku",
            "translation": "to write",
            "part": "verb",
            "collocations": ["手紙を書く", "日記を書く"],
            "example": "毎日日記を書くようにしています。",
            "category": "Education",
        },
        {
            "word": "買う",
            "reading": "kau",
            "translation": "to buy",
            "part": "verb",
            "collocations": ["買い物をする", "本を買う"],
            "example": "明日新しい靴を買います。",
            "category": "Shopping",
        },
        {
            "word": "売る",
            "reading": "uru",
            "translation": "to sell",
            "part": "verb",
            "collocations": ["商品を売る", "高く売る"],
            "example": "古い自転車を売りました。",
            "category": "Shopping",
        },
        {
            "word": "好き",
            "reading": "suki",
            "translation": "like / fond of",
            "part": "adjective",
            "collocations": ["好きな食べ物", "好きになる"],
            "example": "私は寿司が好きです。",
            "category": "Emotions",
        },
        {
            "word": "嫌い",
            "reading": "kirai",
            "translation": "dislike / hate",
            "part": "adjective",
            "collocations": ["嫌いな食べ物", "嫌いになる"],
            "example": "私は運動が嫌いではありません。",
            "category": "Emotions",
        },
        {
            "word": "美しい",
            "reading": "utsukushii",
            "translation": "beautiful",
            "part": "adjective",
            "collocations": ["美しい景色", "美しい花"],
            "example": "春には桜がとても美しい。",
            "category": "Nature",
        },
        {
            "word": "大きい",
            "reading": "ookii",
            "translation": "big / large",
            "part": "adjective",
            "collocations": ["大きい家", "大きいサイズ"],
            "example": "その犬はとても大きい。",
            "category": "Description",
        },
        {
            "word": "小さい",
            "reading": "chiisai",
            "translation": "small",
            "part": "adjective",
            "collocations": ["小さい村", "小さい子ども"],
            "example": "彼の手は小さい。",
            "category": "Description",
        },
        {
            "word": "高い",
            "reading": "takai",
            "translation": "high / tall / expensive",
            "part": "adjective",
            "collocations": ["高い山", "値段が高い"],
            "example": "この時計はとても高いです。",
            "category": "Description",
        },
        {
            "word": "安い",
            "reading": "yasui",
            "translation": "cheap / inexpensive",
            "part": "adjective",
            "collocations": ["安い商品", "値段が安い"],
            "example": "この店は安い服が多い。",
            "category": "Shopping",
        },
        {
            "word": "新しい",
            "reading": "atarashii",
            "translation": "new",
            "part": "adjective",
            "collocations": ["新しい車", "新しいアイデア"],
            "example": "昨日新しい本を買いました。",
            "category": "Description",
        },
        {
            "word": "古い",
            "reading": "furui",
            "translation": "old",
            "part": "adjective",
            "collocations": ["古い建物", "古い友人"],
            "example": "これは古い写真です。",
            "category": "Description",
        },
        {
            "word": "早い",
            "reading": "hayai",
            "translation": "fast / early",
            "part": "adjective",
            "collocations": ["早い電車", "時間が早い"],
            "example": "彼は早い時間に起きます。",
            "category": "Description",
        },
        {
            "word": "遅い",
            "reading": "osoi",
            "translation": "late / slow",
            "part": "adjective",
            "collocations": ["遅い時間", "動きが遅い"],
            "example": "今日は遅い電車に乗りました。",
            "category": "Description",
        },
        {
            "word": "便利",
            "reading": "benri",
            "translation": "convenient",
            "part": "adjective",
            "collocations": ["便利な道具", "便利な場所"],
            "example": "このアプリはとても便利です。",
            "category": "Description",
        },
        {
            "word": "大丈夫",
            "reading": "daijoubu",
            "translation": "it's okay / I'm fine",
            "part": "expression",
            "collocations": ["大丈夫ですか", "大丈夫と言う"],
            "example": "怪我はありませんか？大丈夫です。",
            "category": "Conversation",
        },
        {
            "word": "お願いします",
            "reading": "onegaishimasu",
            "translation": "please",
            "part": "expression",
            "collocations": ["よろしくお願いします", "お願いしますと頼む"],
            "example": "注文をお願いします。",
            "category": "Conversation",
        },
        {
            "word": "どこ",
            "reading": "doko",
            "translation": "where",
            "part": "pronoun",
            "collocations": ["どこですか？", "どこにありますか？"],
            "example": "駅はどこですか？",
            "category": "Directions",
        },
        {
            "word": "いくら",
            "reading": "ikura",
            "translation": "how much",
            "part": "interrogative",
            "collocations": ["いくらですか", "値段はいくら"],
            "example": "このリンゴはいくらですか？",
            "category": "Shopping",
        },
    ]

    # Define a list of categories to cycle through when generating duplicates.
    categories = [
        "Greetings", "Daily Life", "Food & Drink", "Travel", "Shopping",
        "Office", "Health", "Family", "Emotions", "Fitness", "Leisure",
        "Technology", "Education", "Weather", "Hobbies", "Home", "Directions",
        "Numbers", "Nature", "Animals", "Time", "Finance", "Grocery", "Tourism",
        "Medical", "Social", "Business", "Media", "Hotel", "Misc"
    ]

    entries = []
    entry_id = 1
    # Determine how many times to duplicate each base entry to reach at least 1000
    duplicate_factor = (1000 + len(base_entries) - 1) // len(base_entries)
    for i, base in enumerate(base_entries):
        for j in range(duplicate_factor):
            # Copy base entry and assign unique ID and possibly adjust the
            # category.  Use modulo to pick a category from the predefined
            # categories so that duplicates get distributed across topics.
            new_entry = base.copy()
            new_entry["id"] = entry_id
            new_entry["category"] = categories[(i * duplicate_factor + j) % len(categories)]
            entries.append(new_entry)
            entry_id += 1
            if entry_id > 1000:
                break
        if entry_id > 1000:
            break

    # Ensure output directories exist
    os.makedirs('data', exist_ok=True)
    os.makedirs('static', exist_ok=True)

    # Write to vocab.json
    with open('data/vocab.json', 'w', encoding='utf-8') as f_json:
        json.dump(entries, f_json, ensure_ascii=False, indent=2)

    # Also generate a JavaScript file that defines a constant containing
    # the vocabulary array.  This allows the static site to load the
    # vocabulary without requiring a web server or cross‑origin requests.
    vocab_js_path = os.path.join('static', 'vocab.js')
    with open(vocab_js_path, 'w', encoding='utf-8') as f_js:
        f_js.write('const vocab = ')
        json.dump(entries, f_js, ensure_ascii=False, indent=2)
        f_js.write(';\n')

    print(f"Generated {len(entries)} vocabulary entries and wrote data/vocab.json and static/vocab.js.")


if __name__ == '__main__':
    generate_vocab()