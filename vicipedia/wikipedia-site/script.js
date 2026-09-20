/* =========================================================
   VICIPÉDIA — motor de busca
   Lê arquivos .txt da pasta /artigos e exibe como verbetes.
   ========================================================= */

const PASTA_ARTIGOS = "artigos/";
const ARQUIVO_INDICE = PASTA_ARTIGOS + "indice.json";

// Referências de elementos ---------------------------------------------

const form = document.getElementById("form-busca");
const campoBusca = document.getElementById("campo-busca");
const linkInicio = document.getElementById("link-inicio");

const telaInicio = document.getElementById("tela-inicio");
const telaArtigo = document.getElementById("tela-artigo");
const telaVazio = document.getElementById("tela-vazio");
const telaCarregando = document.getElementById("tela-carregando");

const listaSugestoes = document.getElementById("lista-sugestoes");
const listaParecidos = document.getElementById("lista-parecidos");

const artigoCategoria = document.getElementById("artigo-categoria");
const artigoTitulo = document.getElementById("artigo-titulo");
const artigoCorpo = document.getElementById("artigo-corpo");
const blocoVejaTambem = document.getElementById("artigo-veja-tambem");
const listaVejaTambem = document.getElementById("lista-veja-tambem");
const vazioMensagem = document.getElementById("vazio-mensagem");

// Cache em memória dos artigos já carregados -----------------------------
// Cada entrada: { arquivo, titulo, categoria, tags[], corpo, vejaTambem[] }
let bancoDeArtigos = [];
let indiceCarregado = false;

// ---------------------------------------------------------------------
// Utilidades de texto
// ---------------------------------------------------------------------

function normalizar(texto) {
  return texto
    .toLowerCase()
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "") // remove acentos
    .trim();
}

function slugParaLegivel(slug) {
  return slug
    .replace(/\.txt$/i, "")
    .replace(/-/g, " ")
    .replace(/\b\w/g, (c) => c.toUpperCase());
}

// ---------------------------------------------------------------------
// Carregamento dos arquivos
// ---------------------------------------------------------------------

async function carregarIndice() {
  const resposta = await fetch(ARQUIVO_INDICE);
  if (!resposta.ok) {
    throw new Error("Não foi possível ler o índice de artigos (indice.json).");
  }
  return resposta.json();
}

// Faz o parse do formato dos .txt:
// TITULO: ...
// CATEGORIA: ...
// TAGS: a, b, c
// <linha em branco>
// <corpo em texto livre, com "Título de seção" isolado em uma linha
//  tratado como subtítulo>
// VEJA_TAMBEM: slug1, slug2
function interpretarConteudo(nomeArquivo, textoBruto) {
  const linhas = textoBruto.replace(/\r\n/g, "\n").split("\n");

  let titulo = slugParaLegivel(nomeArquivo);
  let categoria = "Geral";
  let tags = [];
  let vejaTambem = [];
  const linhasCorpo = [];

  for (const linha of linhas) {
    if (linha.startsWith("TITULO:")) {
      titulo = linha.slice("TITULO:".length).trim();
    } else if (linha.startsWith("CATEGORIA:")) {
      categoria = linha.slice("CATEGORIA:".length).trim();
    } else if (linha.startsWith("TAGS:")) {
      tags = linha
        .slice("TAGS:".length)
        .split(",")
        .map((t) => t.trim())
        .filter(Boolean);
    } else if (linha.startsWith("VEJA_TAMBEM:")) {
      vejaTambem = linha
        .slice("VEJA_TAMBEM:".length)
        .split(",")
        .map((t) => t.trim())
        .filter((t) => t && t.toLowerCase() !== "nenhum");
    } else {
      linhasCorpo.push(linha);
    }
  }

  // Remove linhas em branco do início do corpo
  while (linhasCorpo.length && linhasCorpo[0].trim() === "") {
    linhasCorpo.shift();
  }

  return {
    arquivo: nomeArquivo,
    slug: nomeArquivo.replace(/\.txt$/i, ""),
    titulo,
    categoria,
    tags,
    vejaTambem,
    corpoBruto: linhasCorpo.join("\n"),
    textoParaBusca: normalizar(
      [titulo, categoria, tags.join(" "), linhasCorpo.join(" ")].join(" ")
    ),
  };
}

// Converte o corpo em parágrafos/listas/subtítulos em HTML seguro
function corpoParaHtml(corpoBruto) {
  const blocos = corpoBruto.split(/\n\s*\n/).map((b) => b.trim()).filter(Boolean);
  let html = "";

  for (const bloco of blocos) {
    const linhasDoBloco = bloco.split("\n").map((l) => l.trim()).filter(Boolean);

    // Bloco de lista numerada (ex: "1. Rômulo...")
    const ehListaNumerada = linhasDoBloco.every((l) => /^\d+[.)]\s/.test(l));
    // Bloco de lista com hífen/traço (ex: "- Senado: ...")
    const ehListaTraco = linhasDoBloco.every((l) => /^[-•]\s/.test(l));

    if (ehListaNumerada) {
      html += "<ol>";
      for (const item of linhasDoBloco) {
        html += `<li>${escaparHtml(item.replace(/^\d+[.)]\s/, ""))}</li>`;
      }
      html += "</ol>";
    } else if (ehListaTraco) {
      html += "<ul>";
      for (const item of linhasDoBloco) {
        html += `<li>${escaparHtml(item.replace(/^[-•]\s/, ""))}</li>`;
      }
      html += "</ul>";
    } else if (
      linhasDoBloco.length === 1 &&
      linhasDoBloco[0].length < 60 &&
      !linhasDoBloco[0].endsWith(".")
    ) {
      // Linha curta isolada sem ponto final = tratada como subtítulo de seção
      html += `<h2>${escaparHtml(linhasDoBloco[0])}</h2>`;
    } else {
      html += `<p>${escaparHtml(linhasDoBloco.join(" "))}</p>`;
    }
  }

  return html;
}

function escaparHtml(texto) {
  const div = document.createElement("div");
  div.textContent = texto;
  return div.innerHTML;
}

// ---------------------------------------------------------------------
// Garante que todos os artigos do índice estejam carregados em memória
// ---------------------------------------------------------------------

async function garantirBancoCarregado() {
  if (indiceCarregado) return;

  mostrarTela("carregando");

  const nomesArquivos = await carregarIndice();

  const resultados = await Promise.allSettled(
    nomesArquivos.map(async (nome) => {
      const resposta = await fetch(PASTA_ARTIGOS + nome);
      if (!resposta.ok) {
        throw new Error(`Falha ao ler ${nome}`);
      }
      const texto = await resposta.text();
      return interpretarConteudo(nome, texto);
    })
  );

  bancoDeArtigos = resultados
    .filter((r) => r.status === "fulfilled")
    .map((r) => r.value);

  indiceCarregado = true;
}

// ---------------------------------------------------------------------
// Busca
// ---------------------------------------------------------------------

function buscarArtigoExato(consultaNormalizada) {
  // 1) título bate exatamente
  let achado = bancoDeArtigos.find(
    (a) => normalizar(a.titulo) === consultaNormalizada
  );
  if (achado) return achado;

  // 2) slug do arquivo bate exatamente
  achado = bancoDeArtigos.find(
    (a) => normalizar(a.slug.replace(/-/g, " ")) === consultaNormalizada
  );
  if (achado) return achado;

  // 3) alguma tag bate exatamente
  achado = bancoDeArtigos.find((a) =>
    a.tags.some((tag) => normalizar(tag) === consultaNormalizada)
  );
  return achado || null;
}

function buscarArtigosParecidos(consultaNormalizada) {
  if (!consultaNormalizada) return [];

  return bancoDeArtigos
    .map((a) => ({ artigo: a, pontos: pontuarRelevancia(a, consultaNormalizada) }))
    .filter((r) => r.pontos > 0)
    .sort((a, b) => b.pontos - a.pontos)
    .map((r) => r.artigo);
}

function pontuarRelevancia(artigo, consultaNormalizada) {
  let pontos = 0;
  const tituloNorm = normalizar(artigo.titulo);

  if (tituloNorm.includes(consultaNormalizada)) pontos += 10;
  if (artigo.tags.some((t) => normalizar(t).includes(consultaNormalizada))) pontos += 6;
  if (artigo.textoParaBusca.includes(consultaNormalizada)) pontos += 2;

  // Também soma pontos por palavra individual da consulta
  const palavras = consultaNormalizada.split(/\s+/).filter((p) => p.length > 2);
  for (const palavra of palavras) {
    if (tituloNorm.includes(palavra)) pontos += 3;
    if (artigo.textoParaBusca.includes(palavra)) pontos += 1;
  }

  return pontos;
}

// ---------------------------------------------------------------------
// Renderização de telas
// ---------------------------------------------------------------------

function mostrarTela(nome) {
  telaInicio.classList.add("oculto");
  telaArtigo.classList.add("oculto");
  telaVazio.classList.add("oculto");
  telaCarregando.classList.add("oculto");

  if (nome === "inicio") telaInicio.classList.remove("oculto");
  if (nome === "artigo") telaArtigo.classList.remove("oculto");
  if (nome === "vazio") telaVazio.classList.remove("oculto");
  if (nome === "carregando") telaCarregando.classList.remove("oculto");

  window.scrollTo({ top: 0, behavior: "instant" in window ? "instant" : "auto" });
}

function renderizarSugestoesIniciais() {
  listaSugestoes.innerHTML = "";
  for (const artigo of bancoDeArtigos) {
    const li = document.createElement("li");
    const a = document.createElement("a");
    a.href = "#";
    a.dataset.slug = artigo.slug;
    a.innerHTML = `${escaparHtml(artigo.titulo)}<span class="cat">${escaparHtml(artigo.categoria)}</span>`;
    li.appendChild(a);
    listaSugestoes.appendChild(li);
  }
}

function renderizarArtigo(artigo) {
  artigoCategoria.textContent = artigo.categoria;
  artigoTitulo.textContent = artigo.titulo;
  artigoCorpo.innerHTML = corpoParaHtml(artigo.corpoBruto);

  listaVejaTambem.innerHTML = "";
  const relacionadosValidos = artigo.vejaTambem
    .map((slug) => bancoDeArtigos.find((a) => a.slug === slug))
    .filter(Boolean);

  if (relacionadosValidos.length > 0) {
    blocoVejaTambem.classList.remove("oculto");
    for (const relacionado of relacionadosValidos) {
      const li = document.createElement("li");
      const a = document.createElement("a");
      a.href = "#";
      a.dataset.slug = relacionado.slug;
      a.textContent = relacionado.titulo;
      li.appendChild(a);
      listaVejaTambem.appendChild(li);
    }
  } else {
    blocoVejaTambem.classList.add("oculto");
  }

  document.title = `${artigo.titulo} — Vicipédia`;
  mostrarTela("artigo");
}

function renderizarSemResultado(consultaOriginal) {
  vazioMensagem.textContent = `Não há nenhum arquivo .txt na Vicipédia que fale sobre "${consultaOriginal}".`;

  const parecidos = buscarArtigosParecidos(normalizar(consultaOriginal)).slice(0, 5);
  listaParecidos.innerHTML = "";

  if (parecidos.length > 0) {
    for (const artigo of parecidos) {
      const li = document.createElement("li");
      const a = document.createElement("a");
      a.href = "#";
      a.dataset.slug = artigo.slug;
      a.innerHTML = `${escaparHtml(artigo.titulo)}<span class="cat">${escaparHtml(artigo.categoria)}</span>`;
      li.appendChild(a);
      listaParecidos.appendChild(li);
    }
    listaParecidos.parentElement.classList.remove("oculto");
  } else {
    listaParecidos.parentElement.classList.add("oculto");
  }

  document.title = "Nenhum resultado — Vicipédia";
  mostrarTela("vazio");
}

// ---------------------------------------------------------------------
// Fluxo principal de pesquisa
// ---------------------------------------------------------------------

async function pesquisar(consultaOriginal) {
  const consulta = consultaOriginal.trim();
  if (!consulta) return;

  try {
    await garantirBancoCarregado();
  } catch (erro) {
    vazioMensagem.textContent =
      "Não foi possível carregar os arquivos de artigos. Verifique se o site está sendo aberto por um servidor local (não diretamente pelo arquivo), e se a pasta 'artigos' está no lugar certo.";
    listaParecidos.parentElement.classList.add("oculto");
    mostrarTela("vazio");
    console.error(erro);
    return;
  }

  const consultaNormalizada = normalizar(consulta);
  const artigoExato = buscarArtigoExato(consultaNormalizada);

  if (artigoExato) {
    renderizarArtigo(artigoExato);
    return;
  }

  // Sem correspondência exata: tenta achar o melhor parecido automaticamente
  const parecidos = buscarArtigosParecidos(consultaNormalizada);
  if (parecidos.length > 0 && pontuarRelevancia(parecidos[0], consultaNormalizada) >= 8) {
    renderizarArtigo(parecidos[0]);
    return;
  }

  renderizarSemResultado(consulta);
}

function abrirArtigoPorSlug(slug) {
  const artigo = bancoDeArtigos.find((a) => a.slug === slug);
  if (artigo) {
    campoBusca.value = artigo.titulo;
    renderizarArtigo(artigo);
  }
}

// ---------------------------------------------------------------------
// Eventos
// ---------------------------------------------------------------------

form.addEventListener("submit", (evento) => {
  evento.preventDefault();
  pesquisar(campoBusca.value);
});

linkInicio.addEventListener("click", async (evento) => {
  evento.preventDefault();
  campoBusca.value = "";
  await garantirBancoCarregado().catch(() => {});
  document.title = "Vicipédia — a enciclopédia de arquivos";
  mostrarTela("inicio");
});

// Delegação de clique para links internos gerados dinamicamente
document.addEventListener("click", (evento) => {
  const link = evento.target.closest("a[data-slug]");
  if (!link) return;
  evento.preventDefault();
  abrirArtigoPorSlug(link.dataset.slug);
});

// ---------------------------------------------------------------------
// Inicialização
// ---------------------------------------------------------------------

(async function iniciar() {
  try {
    await garantirBancoCarregado();
    renderizarSugestoesIniciais();
    mostrarTela("inicio");
  } catch (erro) {
    console.error(erro);
    telaInicio.querySelector(".boas-vindas").innerHTML = `
      <h1>Não foi possível carregar a Vicipédia</h1>
      <p class="subtitulo">
        Os arquivos de artigos não puderam ser lidos. Isso costuma acontecer
        quando o arquivo <code>index.html</code> é aberto diretamente no
        navegador (via <code>file://</code>). Abra o site através de um
        servidor local — por exemplo, com a extensão "Live Server" do VS Code,
        ou rodando <code>python -m http.server</code> dentro da pasta do projeto
        e acessando <code>http://localhost:8000</code>.
      </p>
    `;
    mostrarTela("inicio");
  }
})();
