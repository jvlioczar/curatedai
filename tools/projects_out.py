"""Entradas retiradas do catalogo em 2026-11-07 na revisao do criterio "feito com IA".

Nao e importado por projects.py. Para restaurar uma entrada, mova o bloco p(...) de volta
para projects.py, projects_world.py ou projects_web.py.

Motivos:
- chatbot-arena, have-i-been-trained, glaze-nightshade: sites SOBRE IA (avaliar, rastrear ou
  bloquear modelos), nao projetos feitos com ajuda de IA.
- craiyon, elf-tech, graphcast, te-hiku: o projeto e o proprio modelo ou ferramenta de IA,
  nao uma obra feita com ela.
"""
from projects import p

OUT = [
    p("craiyon", "Craiyon (DALL·E mini)", 2022, "Boris Dayma", "websites", ["entertainment", "education"], "cocreated", ["DALL·E mini"],
      "The free, open image generator that produced the wonky nine-image grids which flooded social media in mid-2022, months before the big models opened up.",
      "O gerador de imagens gratuito e aberto que produziu as grades de nove imagens tortas que inundaram as redes em meados de 2022, meses antes de os grandes modelos abrirem.",
      "Dayma trained the model in the open with a small community, kept it free, and put it on a single page anyone could use with no sign-up.",
      "Dayma treinou o modelo às claras com uma pequena comunidade, manteve gratuito e colocou em uma única página que qualquer um usava sem cadastro.",
      "The project that let the public touch image generation first. Its ugliness was part of the charm, and it was never sold as more than it was.",
      "O projeto que deixou o público tocar a geração de imagens primeiro. A feiura fazia parte do charme, e ele nunca foi vendido como mais do que era.",
      url="https://www.craiyon.com", country="United States", also=["illustration"]),

    p("have-i-been-trained", "Have I Been Trained?", 2022, "Spawning (Mat Dryhurst & Holly Herndon)", "websites", ["activism", "public"], "assisted", ["LAION-5B index", "CLIP search"],
      "A search engine that lets artists check whether their work is among the billions of images used to train image generators, and opt out of future training.",
      "Um buscador que deixa artistas checar se seu trabalho está entre os bilhões de imagens usadas para treinar geradores, e sair de treinos futuros.",
      "Two artists built the index of a public dataset, then negotiated with model makers so that the opt-outs collected by the site are honoured.",
      "Dois artistas indexaram um dataset público e negociaram com fabricantes de modelos para que as recusas coletadas no site sejam respeitadas.",
      "AI infrastructure turned toward the people it was built on. Consent as a product, before any law required it.",
      "Infraestrutura de IA voltada para as pessoas sobre as quais foi construída. Consentimento como produto, antes de qualquer lei exigir.",
      url="https://haveibeentrained.com", country="Germany"),

    p("chatbot-arena", "Chatbot Arena", 2023, "LMSYS (UC Berkeley)", "websites", ["science", "public"], "cocreated", ["Elo rating over blind votes"],
      "Two anonymous chatbots answer the same prompt, you pick the better one, and millions of such votes produce the leaderboard the industry watches.",
      "Dois chatbots anônimos respondem ao mesmo prompt, você escolhe o melhor, e milhões desses votos produzem o ranking que a indústria acompanha.",
      "Researchers designed the blind comparison, the rating system and the open data; the public does the judging.",
      "Pesquisadores desenharam a comparação cega, o sistema de pontuação e os dados abertos; o público faz o julgamento.",
      "The most honest measure of AI quality is a human who does not know which model is talking. The site made that a habit.",
      "A medida mais honesta da qualidade de uma IA é um humano que não sabe qual modelo está falando. O site transformou isso em hábito.",
      url="https://arena.ai", country="United States", also=["data"]),

    p("glaze-nightshade", "Glaze & Nightshade", 2023, "Ben Zhao's lab, University of Chicago", "software", ["activism", "public"], "assisted", ["Adversarial perturbation"],
      "Two free tools that let artists protect their images: Glaze hides their style from models, Nightshade poisons unauthorised training. Nightshade was downloaded 250,000 times in five days.",
      "Duas ferramentas gratuitas que deixam artistas proteger suas imagens: o Glaze esconde o estilo dos modelos, o Nightshade envenena treinos não autorizados. O Nightshade foi baixado 250 mil vezes em cinco dias.",
      "Academic researchers built them with artists, published the methods, and kept them free; artists decide what to protect and accept the small visible artifacts.",
      "Pesquisadores acadêmicos as construíram com artistas, publicaram os métodos e as mantiveram gratuitas; os artistas decidem o que proteger e aceitam os pequenos artefatos visíveis.",
      "AI research pointed at AI, on the artists' side. The clearest example of the technology being used to say no.",
      "Pesquisa em IA apontada para a IA, do lado dos artistas. O exemplo mais claro da tecnologia usada para dizer não.",
      url="https://glaze.cs.uchicago.edu", country="United States"),

    p("elf-tech", "Elf.Tech", 2023, "Grimes", "music", ["entertainment"], "cocreated", ["Elf.Tech (Triniti)"],
      "Grimes released a tool that turns any recording into her voice and promised fifty percent of royalties to anyone who makes a successful song with it.",
      "Grimes lançou uma ferramenta que transforma qualquer gravação na voz dela e prometeu cinquenta por cento dos royalties a quem fizer uma música de sucesso com ela.",
      "The artist chose to open her voice, set the terms, and curated the songs that came back; the fans wrote and sang the material that the model re-voiced.",
      "A artista escolheu abrir a própria voz, definiu os termos e curou as músicas que voltaram; os fãs escreveram e cantaram o material que o modelo revozeou.",
      "The opposite of the unauthorised AI Drake track that prompted it: consent, credit and a split, written down before anyone pressed generate.",
      "O oposto da faixa não autorizada de AI Drake que a motivou: consentimento, crédito e divisão, escritos antes de alguém apertar gerar.",
      url="https://elf.tech", country="Canada"),

    p("graphcast", "GraphCast", 2023, "Google DeepMind", "data", ["science", "public"], "assisted", ["GraphCast (graph neural network)"],
      "A weather model that produces ten-day global forecasts in under a minute and beat the leading physics-based system on about ninety percent of the measures tested.",
      "Um modelo meteorológico que produz previsões globais de dez dias em menos de um minuto e superou o principal sistema baseado em física em cerca de noventa por cento das medidas testadas.",
      "Trained on four decades of reanalysis data from the European weather centre, published in Science with open code, and run alongside traditional forecasts by meteorologists who still make the call.",
      "Treinado com quatro décadas de dados de reanálise do centro meteorológico europeu, publicado na Science com código aberto e rodado ao lado das previsões tradicionais por meteorologistas que ainda dão a palavra final.",
      "Useful in the plainest sense: earlier warnings of cyclones and extreme weather. The paper says what it cannot do, and the forecasters keep the responsibility.",
      "Útil no sentido mais simples: avisos mais cedo de ciclones e tempo extremo. O artigo diz o que o modelo não faz, e os meteorologistas mantêm a responsabilidade.",
      url="https://deepmind.google/blog/graphcast-ai-model-for-faster-and-more-accurate-global-weather-forecasting/", country="United Kingdom"),

    p("te-hiku", "Te Hiku Media speech tools", 2018, "Te Hiku Media", "software", ["culture", "public"], "assisted", ["Custom speech recognition"],
      "A Māori broadcaster built its own speech recognition for te reo Māori from recordings donated by the community, under a data licence the community controls.",
      "Uma emissora maori construiu o próprio reconhecimento de fala para o te reo Māori a partir de gravações doadas pela comunidade, sob uma licença de dados que a comunidade controla.",
      "Thousands of speakers recorded phrases; elders checked pronunciation; the organisation wrote a licence that keeps the data under Māori guardianship.",
      "Milhares de falantes gravaram frases; anciãos checaram a pronúncia; a organização escreveu uma licença que mantém os dados sob guarda maori.",
      "The opposite of scraping. A model that exists to keep a language alive, owned by the people who speak it.",
      "O oposto da raspagem. Um modelo que existe para manter uma língua viva, de propriedade das pessoas que a falam.",
      url="https://tehiku.nz", country="New Zealand"),
]
