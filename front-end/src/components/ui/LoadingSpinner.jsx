export default function LoadingSpinner({ text = 'Cargando...' }) {
  return (
    <div className="loading-spinner">
      <div className="spinner" />
      <span>{text}</span>
    </div>
  )
}
