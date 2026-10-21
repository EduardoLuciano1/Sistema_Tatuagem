const API = 'http://127.0.0.1:8000'
const formLogin = document.getElementById('form-login')

formLogin.addEventListener('submit', async (e) => {
  e.preventDefault()

  const dados = {
    email: document.getElementById('email').value,
    senha: document.getElementById('senha').value
  }

  try {
    const resposta = await fetch(`${API}/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(dados)
    })

    const resultado = await resposta.json()

    if (resposta.ok) {
      localStorage.setItem('token', resultado.access_token)
      window.location.href = 'dashboard.html'
      return
    }

    const mensagem = resultado.detail || resultado.erro || 'Dados inválidos'
    alert('Erro ao entrar: ' + mensagem)
  } catch (erro) {
    console.error('Erro no login:', erro)
    alert('Não foi possível conectar com a API. Verifique se o backend está rodando.')
  }
})
