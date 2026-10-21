const API = 'http://127.0.0.1:8000'
const formTatuador = document.getElementById('form-tatuador')
const botaoSubmit = document.getElementById('btn-submit-tatuador')

protegerPagina()

async function carregarSenioridades() {
  const resposta = await fetchAutenticado(`${API}/senioridade`)
  const senioridades = await resposta.json()
  const select = document.getElementById('idsenioridade')
  select.innerHTML = '<option value="">Selecione...</option>'

  senioridades.forEach(s => {
    const option = document.createElement('option')
    option.value = s.idsenioridade
    option.textContent = s.nome
    select.appendChild(option)
  })
}

async function carregarEstilos() {
  const resposta = await fetchAutenticado(`${API}/estilos`)
  const estilos = await resposta.json()
  const container = document.getElementById('lista-estilos')
  container.innerHTML = ''

  estilos.forEach(e => {
    const checkbox = document.createElement('label')
    checkbox.className = 'btn btn-sm btn-outline-secondary'
    checkbox.innerHTML = `
      <input type="checkbox" value="${e.idestilo}" class="me-1">
      ${e.descricao}
    `
    container.appendChild(checkbox)
  })
}

async function listarTatuadores() {
  const resposta = await fetchAutenticado(`${API}/tatuadores`)
  const tatuadores = await resposta.json()

  const corpo = document.getElementById('corpo-tabela')
  corpo.innerHTML = ''

  tatuadores.forEach(t => {
    corpo.innerHTML += `
      <tr>
        <td>${t.idtatuador}</td>
        <td>${t.nometatuador}</td>
        <td>${t.cpf}</td>
        <td>${t.email ?? '-'}</td>
        <td>${t.telefone ?? '-'}</td>
        <td>${t.senioridade ?? '-'}</td>
        <td>${(t.estilos || []).map(e => e.descricao).join(', ') || '-'}</td>
        <td>
          <button class="btn btn-sm btn-warning me-2" onclick='preencherFormularioEdicao(${JSON.stringify(t)})'>Editar</button>
          <button class="btn btn-sm btn-danger" onclick="deletarTatuador(${t.idtatuador})">Excluir</button>
        </td>
      </tr>`
  })
}

function limparFormulario() {
  formTatuador.reset()
  delete formTatuador.dataset.idTatuador
  botaoSubmit.textContent = 'Cadastrar'
  botaoSubmit.classList.remove('btn-success')
  botaoSubmit.classList.add('btn-primary')
  document.querySelectorAll('#lista-estilos input').forEach(input => input.checked = false)
}

async function preencherFormularioEdicao(tatuador) {
  document.getElementById('nometatuador').value = tatuador.nometatuador
  document.getElementById('cpf').value = tatuador.cpf
  document.getElementById('email').value = tatuador.email || ''
  document.getElementById('telefone').value = tatuador.telefone || ''
  document.getElementById('datacontratacao').value = tatuador.datacontratacao || ''
  document.getElementById('idsenioridade').value = tatuador.idsenioridade
  formTatuador.dataset.idTatuador = tatuador.idtatuador

  const resposta = await fetchAutenticado(`${API}/tatuadores/${tatuador.idtatuador}/estilos`)
  const estilos = await resposta.json()
  const estilosMarcados = new Set(estilos.map(e => Number(e.idestilo)))

  document.querySelectorAll('#lista-estilos input').forEach(input => {
    input.checked = estilosMarcados.has(Number(input.value))
  })

  botaoSubmit.textContent = 'Salvar alteração'
  botaoSubmit.classList.remove('btn-primary')
  botaoSubmit.classList.add('btn-success')
}

formTatuador.addEventListener('submit', async (e) => {
  e.preventDefault()

  const tatuador = {
    nometatuador: document.getElementById('nometatuador').value,
    cpf: document.getElementById('cpf').value,
    email: document.getElementById('email').value || null,
    telefone: document.getElementById('telefone').value || null,
    datacontratacao: document.getElementById('datacontratacao').value || null,
    idsenioridade: Number(document.getElementById('idsenioridade').value)
  }

  const estilosSelecionados = Array.from(document.querySelectorAll('#lista-estilos input:checked')).map(i => Number(i.value))
  const idTatuador = formTatuador.dataset.idTatuador

  let resposta
  if (idTatuador) {
    resposta = await fetchAutenticado(`${API}/tatuadores/${idTatuador}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(tatuador)
    })
  } else {
    resposta = await fetchAutenticado(`${API}/tatuadores`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(tatuador)
    })
  }

  const dados = await resposta.json().catch(() => ({}))
  const idParaEstilos = idTatuador || dados.idtatuador

  if (idParaEstilos) {
    await fetchAutenticado(`${API}/tatuadores/${idParaEstilos}/estilos`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(estilosSelecionados)
    })
  }

  limparFormulario()
  listarTatuadores()
})

async function deletarTatuador(id) {
  if (!confirm('Tem certeza que deseja excluir este tatuador?')) return
  await fetchAutenticado(`${API}/tatuadores/${id}`, { method: 'DELETE' })
  listarTatuadores()
}

(async function init() {
  await carregarSenioridades()
  await carregarEstilos()
  await listarTatuadores()
})()
