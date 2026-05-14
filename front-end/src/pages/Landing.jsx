import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import './Landing.css'

const FEATURES = [
  {
    icon: 'M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4',
    title: 'Gestión de Encomiendas',
    desc: 'Registra, edita y da seguimiento a cada paquete desde una plataforma centralizada con generación automática de guías.',
  },
  {
    icon: 'M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4',
    title: 'Tracking en Tiempo Real',
    desc: 'Clientes y operadores pueden rastrear cada envío con una línea de tiempo visual paso a paso, desde el registro hasta la entrega.',
  },
  {
    icon: 'M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7',
    title: 'Logística y Rutas',
    desc: 'Asigna lotes a vehículos y conductores, visualiza rutas y optimiza la distribución con interfaz drag-and-drop.',
  },
  {
    icon: 'M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z',
    title: 'Comprobantes Digitales',
    desc: 'Captura firmas y fotos como prueba de entrega. Cada comprobante queda registrado con geolocalización y timestamp.',
  },
  {
    icon: 'M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z',
    title: 'Reportes y Analítica',
    desc: 'Visualiza KPIs, volumen diario, distribución por estado y rendimiento por ruta con gráficos interactivos y exportación CSV.',
  },
  {
    icon: 'M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z',
    title: 'Multi-Rol y Permisos',
    desc: 'Cuatro roles predefinidos (Admin, Operador, Conductor, Cliente) con menús y funcionalidades adaptadas a cada perfil.',
  },
]

const STEPS = [
  { number: '01', title: 'Registra el Envío', desc: 'Ingresa los datos del remitente, destinatario y paquete. El sistema genera automáticamente un número de guía único con código QR y código de barras.' },
  { number: '02', title: 'Asigna a una Ruta', desc: 'Agrupa los paquetes en lotes y asígnalos a un vehículo y conductor disponible desde el panel de logística.' },
  { number: '03', title: 'Tracking Automático', desc: 'Cada escaneo actualiza el estado en tiempo real. El cliente recibe notificaciones y puede rastrear desde cualquier dispositivo.' },
  { number: '04', title: 'Entrega y Comprobante', desc: 'El conductor registra la entrega con firma digital o foto. El comprobante queda almacenado con GPS y timestamp.' },
]

const TESTIMONIALS = [
  { name: 'María Soto', role: 'Gerente de Operaciones', company: 'Distribuidora Los Andes, Valencia', quote: 'Redujimos nuestros tiempos de entrega en un 40% desde que implementamos AWEN. La trazabilidad es increíble.' },
  { name: 'Carlos Muñoz', role: 'Director General', company: 'TechStore Venezuela, Caracas', quote: 'El módulo de tracking nos ha permitido darle a nuestros clientes la transparencia que necesitaban. Altamente recomendado.' },
  { name: 'Ana López', role: 'Jefa de Logística', company: 'Cadena Fármaco Centro, Maracay', quote: 'La interfaz es intuitiva y el equipo de soporte siempre responde rápido. Una herramienta que transformó nuestra logística.' },
]

const NAV_LINKS = [
  { label: 'Características', href: '#features' },
  { label: 'Cómo Funciona', href: '#how-it-works' },
  { label: 'Precios', href: '#cta' },
  { label: 'Contacto', href: '#contact' },
]

function Navbar() {
  const [scrolled, setScrolled] = useState(false)
  const [menuOpen, setMenuOpen] = useState(false)
  const navigate = useNavigate()

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 20)
    window.addEventListener('scroll', onScroll, { passive: true })
    return () => window.removeEventListener('scroll', onScroll)
  }, [])

  return (
    <nav className={`landing-nav ${scrolled ? 'scrolled' : ''}`}>
      <div className="landing-nav-inner">
        <a href="#" className="landing-logo" onClick={e => { e.preventDefault(); window.scrollTo({ top: 0, behavior: 'smooth' }) }}>
          <div className="landing-logo-mark">A</div>
          <span className="landing-logo-text">AWEN</span>
        </a>
        <div className={`landing-nav-links ${menuOpen ? 'open' : ''}`}>
          {NAV_LINKS.map(link => (
            <a key={link.href} href={link.href} className="landing-nav-link" onClick={() => setMenuOpen(false)}>
              {link.label}
            </a>
          ))}
          <div className="landing-nav-ctas">
            <button className="landing-btn landing-btn-ghost" onClick={() => navigate('/tracking')}>
              Rastrear Envío
            </button>
            <button className="landing-btn landing-btn-primary" onClick={() => navigate('/login')}>
              Iniciar Sesión
            </button>
          </div>
        </div>
        <button className="landing-menu-btn" onClick={() => setMenuOpen(!menuOpen)}>
          <span /><span /><span />
        </button>
      </div>
    </nav>
  )
}

function Hero() {
  const navigate = useNavigate()
  return (
    <section className="landing-hero">
      <div className="landing-hero-bg">
        <div className="landing-hero-glow glow-1" />
        <div className="landing-hero-glow glow-2" />
      </div>
      <div className="landing-hero-content">
        <div className="landing-hero-badge">Plataforma integral de logística</div>
        <h1 className="landing-hero-title">
          Gestiona tus envíos nacionales<br />
          <span className="text-gradient">con precisión quirúrgica</span>
        </h1>
        <p className="landing-hero-subtitle">
          La plataforma todo-en-uno para empresas de mensajería y encomiendas en Venezuela.
          Desde el registro hasta la entrega, cada paso está controlado.
        </p>
        <div className="landing-hero-ctas">
          <button className="landing-btn landing-btn-primary landing-btn-lg" onClick={() => navigate('/login')}>
            Comenzar Ahora
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5"><path d="M5 12h14m-7-7l7 7-7 7"/></svg>
          </button>
          <button className="landing-btn landing-btn-outline landing-btn-lg" onClick={() => navigate('/tracking')}>
            Rastrear Envío
          </button>
        </div>
      </div>
      <div className="landing-hero-visual">
        <div className="dashboard-mockup">
          <div className="mockup-header">
            <div className="mockup-dots"><span /><span /><span /></div>
            <div className="mockup-title">Dashboard</div>
          </div>
          <div className="mockup-body">
            <div className="mockup-stats">
              {[['48', 'Envíos Hoy'], ['23', 'En Tránsito'], ['18', 'Entregados']].map(([v, l]) => (
                <div key={l} className="mockup-stat"><div className="mockup-stat-val">{v}</div><div className="mockup-stat-lbl">{l}</div></div>
              ))}
            </div>
            <div className="mockup-chart">
              <div className="mockup-chart-line">
                {[40, 65, 45, 80, 55, 70, 35].map((h, i) => (
                  <div key={i} className="mockup-bar" style={{ height: `${h}%` }} />
                ))}
              </div>
            </div>
            <div className="mockup-table">
              <div className="mockup-row"><span>AWEN-2026-0001</span><span className="badge-transit">En Tránsito</span></div>
              <div className="mockup-row"><span>AWEN-2026-0002</span><span className="badge-done">Entregado</span></div>
              <div className="mockup-row"><span>AWEN-2026-0003</span><span className="badge-reg">Registrado</span></div>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}

function StatsBar() {
  return (
    <section className="landing-stats">
      <div className="landing-stats-inner">
        {[
          { value: '12,450+', label: 'Envíos Gestionados' },
          { value: '6', label: 'Sucursales' },
          { value: '98.2%', label: 'Tasa de Éxito' },
          { value: '24/7', label: 'Soporte' },
        ].map(s => (
          <div key={s.label} className="landing-stat">
            <span className="landing-stat-value">{s.value}</span>
            <span className="landing-stat-label">{s.label}</span>
          </div>
        ))}
      </div>
    </section>
  )
}

function Features() {
  return (
    <section id="features" className="landing-section landing-features landing-scroll-target">
      <div className="landing-section-header">
        <span className="landing-section-tag">Características</span>
        <h2>Todo lo que necesitas para gestionar tu operación</h2>
        <p>Una plataforma completa diseñada para empresas de mensajería y courier nacional.</p>
      </div>
      <div className="landing-features-grid">
        {FEATURES.map(f => (
          <div key={f.title} className="landing-feature-card">
            <div className="landing-feature-icon">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
                <path d={f.icon} />
              </svg>
            </div>
            <h3>{f.title}</h3>
            <p>{f.desc}</p>
          </div>
        ))}
      </div>
    </section>
  )
}

function HowItWorks() {
  return (
    <section id="how-it-works" className="landing-section landing-how landing-scroll-target">
      <div className="landing-section-header">
        <span className="landing-section-tag">Proceso</span>
        <h2>Así de simple funciona AWEN</h2>
        <p>Cuatro pasos para transformar tu operación logística.</p>
      </div>
      <div className="landing-steps">
        {STEPS.map((s, i) => (
          <div key={s.number} className="landing-step">
            <div className="landing-step-number">{s.number}</div>
            <div className="landing-step-content">
              <h3>{s.title}</h3>
              <p>{s.desc}</p>
            </div>
            {i < STEPS.length - 1 && <div className="landing-step-connector" />}
          </div>
        ))}
      </div>
    </section>
  )
}

function Testimonials() {
  return (
    <section className="landing-section landing-testimonials">
      <div className="landing-section-header">
        <span className="landing-section-tag">Testimonios</span>
        <h2>Lo que dicen nuestros clientes</h2>
      </div>
      <div className="landing-testimonials-grid">
        {TESTIMONIALS.map(t => (
          <div key={t.name} className="landing-testimonial-card">
            <div className="landing-testimonial-quote">"</div>
            <p className="landing-testimonial-text">{t.quote}</p>
            <div className="landing-testimonial-author">
              <div className="landing-testimonial-avatar">{t.name.split(' ').map(w => w[0]).join('')}</div>
              <div>
                <strong>{t.name}</strong>
                <span>{t.role}, {t.company}</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </section>
  )
}

function CtaSection() {
  const navigate = useNavigate()
  return (
    <section id="cta" className="landing-cta landing-scroll-target">
      <div className="landing-cta-bg">
        <div className="landing-cta-glow" />
      </div>
      <div className="landing-cta-content">
        <h2>¿Listo para optimizar tu operación?</h2>
        <p>Únete a las empresas que ya confían en AWEN para gestionar sus envíos nacionales.</p>
        <div className="landing-cta-buttons">
          <button className="landing-btn landing-btn-primary landing-btn-lg" onClick={() => navigate('/login')}>
            Solicitar Demo
          </button>
          <button className="landing-btn landing-btn-outline landing-btn-lg landing-btn-white" onClick={() => navigate('/tracking')}>
            Rastrear un Envío
          </button>
        </div>
      </div>
    </section>
  )
}

function Footer() {
  return (
    <footer id="contact" className="landing-footer landing-scroll-target">
      <div className="landing-footer-inner">
        <div className="landing-footer-brand">
          <div className="landing-logo">
            <div className="landing-logo-mark">A</div>
            <span className="landing-logo-text">AWEN</span>
          </div>
          <p>Plataforma integral de gestión logística para empresas de mensajería y encomiendas a nivel nacional en Venezuela.</p>
        </div>
        <div className="landing-footer-links">
          <div className="landing-footer-col">
            <h4>Producto</h4>
            <a href="#features">Características</a>
            <a href="#how-it-works">Cómo Funciona</a>
            <a href="#cta">Precios</a>
          </div>
          <div className="landing-footer-col">
            <h4>Compañía</h4>
            <a href="#">Sobre Nosotros</a>
            <a href="#">Blog</a>
            <a href="#contact">Contacto</a>
          </div>
          <div className="landing-footer-col">
            <h4>Soporte</h4>
            <a href="#">Centro de Ayuda</a>
            <a href="#">Documentación API</a>
            <a href="#">Estado del Sistema</a>
          </div>
          <div className="landing-footer-col landing-footer-contact">
            <h4>Contacto</h4>
            <a href="tel:+584244504195">+58 (424) 450.4195</a>
            <a href="mailto:AtencionCliente@awen.com">AtencionCliente@awen.com</a>
            <span className="landing-footer-address">Municipio San Diego, Urb. Yuma II, Calle No. 3</span>
          </div>
        </div>
      </div>
      <div className="landing-footer-bottom">
        <span>&copy; {new Date().getFullYear()} AWEN. Todos los derechos reservados.</span>
      </div>
    </footer>
  )
}

export default function Landing() {
  return (
    <div className="landing-page">
      <Navbar />
      <Hero />
      <StatsBar />
      <Features />
      <HowItWorks />
      <Testimonials />
      <CtaSection />
      <Footer />
    </div>
  )
}
