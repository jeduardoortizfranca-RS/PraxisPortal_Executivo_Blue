(function () {
  // ✅ Base da API — domínio oficial da Vercel
  const API_BASE =
    window.API_URL || "https://praxis-portal-executivo-blue-8t5ow1ce5.vercel.app";
  window.__API_BASE__ = API_BASE;

  // ✅ Gerenciar token JWT
  function saveToken(token) {
    if (token) localStorage.setItem("jwt", token);
  }
  function getToken() {
    return localStorage.getItem("jwt") || "";
  }
  function clearToken() {
    localStorage.removeItem("jwt");
  }

  // Função para redirecionar para a página de login e limpar o token
  function redirectToLogin() {
    clearToken(); // Limpa qualquer token inválido
    window.location.href = "/frontend/index.html";
  }

  // ✅ Exibe mensagem no card
  function showMessage(msg, color = "#2563eb") {
    const div = document.getElementById("msg");
    if (!div) return;
    div.style.color = color;
    div.textContent = msg;
  }

  // ✅ Login
  async function handleLogin(event) {
    event.preventDefault();
    const username = document.getElementById("email").value.trim();
    const password = document.getElementById("senha").value.trim();

    showMessage("Realizando login...");
    try {
      const res = await fetch(`${API_BASE}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
	body: JSON.stringify({ email: username, password })
      });

      const data = await res.json(); // Tenta parsear o JSON da resposta
      
      if (!res.ok) {
        // ✅ CORREÇÃO: Lógica mais robusta para extrair a mensagem de erro
        let errorMessage = "Falha no login. Credenciais inválidas ou erro no servidor.";

        if (data) {
          if (typeof data.detail === 'string') {
            errorMessage = data.detail;
          } else if (Array.isArray(data.detail) && data.detail.length > 0 && data.detail[0].msg) {
            // Caso de erro de validação do FastAPI (detail é uma lista de objetos)
            errorMessage = data.detail.map(err => err.msg).join(", ");
          } else if (typeof data === 'object' && data !== null) {
            // Se o 'data' inteiro for um objeto e não tiver 'detail' string, tenta stringify
            errorMessage = JSON.stringify(data);
          }
        }
        showMessage(`❌ ${errorMessage}`, "red");
        return;
      }

      const token = data?.access_token || data?.token;
      if (!token) {
        showMessage("❌ Token não recebido da API.", "red");
        return;
      }
      saveToken(token);
      showMessage("✅ Login bem-sucedido!");
      console.log("Token salvo:", token);

      setTimeout(() => {
        window.location.href = "/frontend/financeiro.html";
      }, 800);
    } catch (err) {
      console.error("Erro no login:", err);
      showMessage("Erro de conexão com o servidor.", "red");
    }
  }

  // ✅ Função para verificar o token (essencial para proteger o dashboard)
  async function verifyToken() {
    const token = getToken();
    if (!token) {
      redirectToLogin();
      return;
    }

    try {
      const res = await fetch(`${API_BASE}/auth/verify`, {
        method: "GET",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (!res.ok) {
        redirectToLogin();
        return;
      }
    } catch (error) {
      console.error("Erro na verificação do token:", error);
      redirectToLogin();
    }
  }

  // ✅ Botões extras
  function showCurrentToken() {
    const token = getToken();
    showMessage(token ? `Token salvo: ${token.substring(0, 25)}...` : "Nenhum token salvo.");
  }
  function clearCurrentToken() {
    clearToken();
    showMessage("Token removido.");
  }

  // ✅ Eventos
  document.getElementById("loginForm")?.addEventListener("submit", handleLogin);
  document.getElementById("btnShowToken")?.addEventListener("click", showCurrentToken);
  document.getElementById("btnClearToken")?.addEventListener("click", clearCurrentToken);

  // ✅ Executa a verificação do token ao carregar a página (se não for a página de login)
  if (window.location.pathname.includes("financeiro.html")) {
    verifyToken();
  }
})();
