"""Categorias (formato da obra), finalidades (tags) e graus de IA. Cada projeto tem UMA categoria principal."""

# id, nome EN, nome PT, matiz (0-360), descrição EN, descrição PT
CATEGORIES = [
    dict(id="websites", en="Websites & web apps", pt="Sites e web apps", hue=212,
         desc=dict(en="Sites, landing pages, online tools and browser experiences where AI did real work and a human shaped the result.",
                   pt="Sites, landing pages, ferramentas online e experiências no navegador em que a IA fez trabalho de verdade e um humano moldou o resultado.")),
    dict(id="software", en="Software & tools", pt="Software e ferramentas", hue=160,
         desc=dict(en="Apps, extensions, scripts, automations and open-source projects built with or around AI.",
                   pt="Apps, extensões, scripts, automações e projetos open source construídos com ou em torno de IA.")),
    dict(id="games", en="Games & interactive", pt="Jogos e interativos", hue=96,
         desc=dict(en="Games, interactive fiction, simulators and digital toys where AI is a mechanic, not a gimmick.",
                   pt="Jogos, ficção interativa, simuladores e brinquedos digitais em que a IA é mecânica, não truque.")),
    dict(id="video", en="Video & animation", pt="Vídeo e animação", hue=18,
         desc=dict(en="Short films, music videos, animation, motion design and documentaries directed by people and rendered with AI.",
                   pt="Curtas, clipes, animação, motion design e documentários dirigidos por pessoas e renderizados com IA.")),
    dict(id="music", en="Music & audio", pt="Música e áudio", hue=330,
         desc=dict(en="Songs, podcasts, sound design, voice and restoration work where AI served the ear.",
                   pt="Músicas, podcasts, sound design, voz e restauração em que a IA serviu ao ouvido.")),
    dict(id="illustration", en="Illustration & image", pt="Ilustração e imagem", hue=42,
         desc=dict(en="Illustration, comics, concept art, photography and image series with a visible authorial hand.",
                   pt="Ilustração, quadrinhos, concept art, fotografia e séries de imagens com mão autoral visível.")),
    dict(id="design", en="Graphic design & branding", pt="Design gráfico e identidade", hue=280,
         desc=dict(en="Identities, posters, typography, packaging and editorial design that used AI as a studio tool.",
                   pt="Identidades, cartazes, tipografia, embalagem e design editorial que usaram IA como ferramenta de estúdio.")),
    dict(id="writing", en="Writing & publishing", pt="Escrita e publicação", hue=0,
         desc=dict(en="Books, zines, newsletters, journalism, scripts and poetry co-written and edited by humans.",
                   pt="Livros, zines, newsletters, jornalismo, roteiros e poesia coescritos e editados por humanos.")),
    dict(id="education", en="Education & explainers", pt="Educação e explicadores", hue=190,
         desc=dict(en="Courses, interactive explainers, tutors and reference works that teach better because of AI.",
                   pt="Cursos, explicadores interativos, tutores e obras de referência que ensinam melhor por causa da IA.")),
    dict(id="data", en="Data & science", pt="Dados e ciência", hue=240,
         desc=dict(en="Visualizations, datasets, scientific results and maps that only exist because of machine learning.",
                   pt="Visualizações, datasets, resultados científicos e mapas que só existem por causa do aprendizado de máquina.")),
    dict(id="physical", en="3D, product & space", pt="3D, produto e espaço", hue=70,
         desc=dict(en="3D modelling, architecture, fashion, furniture and physical objects designed with AI.",
                   pt="Modelagem 3D, arquitetura, moda, mobiliário e objetos físicos projetados com IA.")),
    dict(id="art", en="Art & experimental", pt="Arte e experimental", hue=300,
         desc=dict(en="Generative art, installations, performances and works that take AI itself as their medium.",
                   pt="Arte generativa, instalações, performances e obras que tomam a própria IA como meio.")),
]

# finalidades: para que serve (tags, um projeto pode ter várias)
PURPOSES = [
    dict(id="entertainment", en="Entertainment", pt="Entretenimento"),
    dict(id="activism", en="Activism & causes", pt="Ativismo e causas"),
    dict(id="education", en="Education", pt="Educação"),
    dict(id="public", en="Public utility & accessibility", pt="Utilidade pública e acessibilidade"),
    dict(id="commercial", en="Commercial", pt="Comercial"),
    dict(id="journalism", en="Journalism & information", pt="Jornalismo e informação"),
    dict(id="personal", en="Personal & memory", pt="Pessoal e memória"),
    dict(id="science", en="Science & health", pt="Ciência e saúde"),
    dict(id="culture", en="Culture & preservation", pt="Cultura e preservação"),
]

# grau de IA: quem fez o quê
DEGREES = [
    dict(id="assisted", en="AI-assisted", pt="Assistido por IA",
         desc=dict(en="AI was a support tool. The work would exist without it, just slower.", pt="A IA foi ferramenta de apoio. A obra existiria sem ela, só que mais devagar.")),
    dict(id="cocreated", en="Co-created", pt="Cocriado",
         desc=dict(en="Human and AI in dialogue. Neither could have made this alone.", pt="Humano e IA em diálogo. Nenhum dos dois faria isso sozinho.")),
    dict(id="directed", en="Human-directed", pt="Dirigido por humano",
         desc=dict(en="AI produced most of the material; a person chose, cut, corrected and signed it.", pt="A IA produziu a maior parte do material; uma pessoa escolheu, cortou, corrigiu e assinou.")),
]

BY_CAT = {c["id"]: c for c in CATEGORIES}
BY_PURPOSE = {p["id"]: p for p in PURPOSES}
BY_DEGREE = {d["id"]: d for d in DEGREES}
