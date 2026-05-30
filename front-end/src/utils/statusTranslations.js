export const PARCEL_STATUS_LABELS = {
  'Registered': 'Registrado',
  'Picked Up': 'Recogido',
  'In Transit': 'En Tránsito',
  'At Destination Branch': 'En Sucursal Destino',
  'Out for Delivery': 'En Reparto',
  'Delivered': 'Entregado',
  'Returned': 'Devuelto',
}

export const BATCH_STATUS_LABELS = {
  'Pending Assignment': 'Pendiente de Asignación',
  'Assigned': 'Asignado',
  'Completed': 'Completado',
}

export const DELIVERY_STATUS_LABELS = {
  'Pending': 'Pendiente',
  'Completed': 'Completado',
}

export const translateStatus = (status) =>
  PARCEL_STATUS_LABELS[status] || BATCH_STATUS_LABELS[status] || DELIVERY_STATUS_LABELS[status] || status
