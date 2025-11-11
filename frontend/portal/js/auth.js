/**
 * Autenticação Portal Praxis AI Core - Integração com Supabase Auth
 * Versão limpa sem referências a marcas externas
 */

class PraxisPortalAuth {
    constructor() {
        this.API_BASE = window.API_URL || "http://localhost:8001";
        this.SUPABASE_URL = window.SUPABASE_URL || "https://seu-projeto.supabase.co";
        this.SUPABASE_KEY = window.SUPABASE_KEY || "sua-chave-anon";
        
        // Inicializar Supabase client
        this.supabase = supabase.createClient(this.SUPABASE_URL, this.SUPABASE_KEY);
        
        this.init();
    }
    
    init() {
        // Configurar eventos quando o DOM carregar
        document.addEventListener('DOMContentLoaded', () => {
            this.setupEventListeners();
            this.checkAuthStatus();
        });
        
        // Monitorar mudanças de autenticação
        this.supabase.auth.onAuthStateChange((event, session) => {
            if (event === 'SIGNED_IN') {
                this.handleSignIn(session);
            } else if (event === 'SIGNED_OUT') {
                this.handleSignOut();
            }
        });
    }
    
    setupEventListeners() {
        // Formulário de login
        const loginForm = document.getElementById('loginForm');
        if (loginForm) {
            loginForm.addEventListener('submit', (e) => this.handleLogin(e));
        }
        
        // Formulário de registro
        const registerForm = document.getElementById('registerForm');
       
