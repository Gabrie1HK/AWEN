export const branches = [
  { id: 1, name: 'Sucursal Central', city: 'Caracas', address: 'Av. Libertador 1234, Urb. El Rosal', manager: 'Carlos Munoz', phone: '+58 212 212 3456', active: true },
  { id: 2, name: 'Sucursal Norte', city: 'Maracaibo', address: 'Calle 72 con Av. 5 de Julio', manager: 'Maria Soto', phone: '+58 261 212 3456', active: true },
  { id: 3, name: 'Sucursal Sur', city: 'Ciudad Guayana', address: 'Av. Principal de Castillito', manager: 'Pedro Torres', phone: '+58 286 212 3456', active: true },
  { id: 4, name: 'Sucursal Este', city: 'Barcelona', address: 'Av. Fuerzas Armadas 2345', manager: 'Ana Lopez', phone: '+58 281 234 5678', active: true },
  { id: 5, name: 'Sucursal Costa', city: 'Maracay', address: 'Av. Las Delicias 678', manager: 'Jose Rivas', phone: '+58 243 212 3456', active: false },
  { id: 6, name: 'Sucursal Occidental', city: 'Barquisimeto', address: 'Av. Vargas con Carrera 19', manager: 'Luis Vargas', phone: '+58 251 212 3456', active: true },
]

export const users = [
  { id: 1, name: 'Admin Principal', email: 'admin@awen.com', role: 'Admin', branch: 'Sucursal Central', phone: '+58 212 212 3456', active: true, lastLogin: '2026-05-12 09:30' },
  { id: 2, name: 'Operador Carlos', email: 'operador.carlos@awen.com', role: 'Warehouse Operator', branch: 'Sucursal Central', phone: '+58 412 123 4567', active: true, lastLogin: '2026-05-13 07:15' },
  { id: 3, name: 'Operador Maria', email: 'operador.maria@awen.com', role: 'Warehouse Operator', branch: 'Sucursal Norte', phone: '+58 416 765 4321', active: true, lastLogin: '2026-05-12 22:40' },
  { id: 4, name: 'Conductor Pedro', email: 'conductor.pedro@awen.com', role: 'Driver', branch: 'Sucursal Central', phone: '+58 414 987 6543', active: true, lastLogin: '2026-05-13 06:00' },
  { id: 5, name: 'Conductor Ana', email: 'conductor.ana@awen.com', role: 'Driver', branch: 'Sucursal Sur', phone: '+58 424 456 7890', active: true, lastLogin: '2026-05-12 18:20' },
  { id: 6, name: 'Cliente Juan', email: 'juan@email.com', role: 'Client', branch: '-', phone: '+58 412 789 0123', address: 'Calle 60 123, Merida', active: true, lastLogin: '2026-05-10 14:00' },
  { id: 7, name: 'Cliente Marta', email: 'marta@email.com', role: 'Client', branch: '-', phone: '+58 414 321 0987', address: 'Av. Bolivar 456, Merida', active: false, lastLogin: '2026-04-28 11:30' },
]

export const parcels = [
  { id: 'ENV-001', guide: 'AWEN-2026-0001', sender: 'TechStore CA', senderId: 'J-12345678-9', senderPhone: '+58 412 123 4567', recipient: 'Roberto Garcia', recipientId: 'V-12345678', recipientPhone: '+58 414 987 6543', recipientAddress: 'Av. Universidad 742, Caracas', originBranch: 'Sucursal Central', destinationBranch: 'Sucursal Norte', weight: 2.5, dimensions: '30x20x15 cm', declaredValue: 150000, description: 'Notebook y accesorios', status: 'In Transit', createdAt: '2026-05-10', updatedAt: '2026-05-13', qrData: 'AWEN-2026-0001', barcode: '|||AWEN-2026-0001|||' },
  { id: 'ENV-002', guide: 'AWEN-2026-0002', sender: 'Distribuidora Sur CA', senderId: 'J-87654321-0', senderPhone: '+58 424 234 5678', recipient: 'Carmen Flores', recipientId: 'V-23456789', recipientPhone: '+58 416 876 5432', recipientAddress: 'Av. Las Americas 456, Ciudad Guayana', originBranch: 'Sucursal Central', destinationBranch: 'Sucursal Sur', weight: 15.0, dimensions: '50x40x30 cm', declaredValue: 450000, description: 'Equipo de sonido profesional', status: 'Delivered', createdAt: '2026-05-08', updatedAt: '2026-05-12', qrData: 'AWEN-2026-0002', barcode: '|||AWEN-2026-0002|||' },
  { id: 'ENV-003', guide: 'AWEN-2026-0003', sender: 'Farmacias del Centro CA', senderId: 'J-78901234-0', senderPhone: '+58 412 345 6789', recipient: 'Dr. Andres Vega', recipientId: 'V-34567890', recipientPhone: '+58 414 765 4321', recipientAddress: 'Av. Bolivar 789, Caracas', originBranch: 'Sucursal Central', destinationBranch: 'Sucursal Central', weight: 0.8, dimensions: '20x15x10 cm', declaredValue: 80000, description: 'Medicamentos controlados', status: 'Registered', createdAt: '2026-05-13', updatedAt: '2026-05-13', qrData: 'AWEN-2026-0003', barcode: '|||AWEN-2026-0003|||' },
  { id: 'ENV-004', guide: 'AWEN-2026-0004', sender: 'ElectroHogar SA', senderId: 'J-45678901-0', senderPhone: '+58 424 456 7890', recipient: 'Laura Martinez', recipientId: 'V-45678901', recipientPhone: '+58 416 654 3210', recipientAddress: 'Av. Las Delicias 234, Maracay', originBranch: 'Sucursal Este', destinationBranch: 'Sucursal Costa', weight: 8.0, dimensions: '60x40x35 cm', declaredValue: 320000, description: 'Aspiradora robot', status: 'At Destination Branch', createdAt: '2026-05-09', updatedAt: '2026-05-13', qrData: 'AWEN-2026-0004', barcode: '|||AWEN-2026-0004|||' },
  { id: 'ENV-005', guide: 'AWEN-2026-0005', sender: 'Libreria Nacional CA', senderId: 'J-23456789-0', senderPhone: '+58 412 567 8901', recipient: 'Patricio Silva', recipientId: 'V-56789012', recipientPhone: '+58 414 543 2109', recipientAddress: 'Calle 77 567, Maracaibo', originBranch: 'Sucursal Central', destinationBranch: 'Sucursal Norte', weight: 3.2, dimensions: '35x25x20 cm', declaredValue: 45000, description: 'Libros y material educativo', status: 'Returned', createdAt: '2026-05-05', updatedAt: '2026-05-11', qrData: 'AWEN-2026-0005', barcode: '|||AWEN-2026-0005|||' },
  { id: 'ENV-006', guide: 'AWEN-2026-0006', sender: 'Moda Urbana CA', senderId: 'J-56789012-0', senderPhone: '+58 424 678 9012', recipient: 'Daniela Rojas', recipientId: 'V-67890123', recipientPhone: '+58 416 432 1098', recipientAddress: 'Av. Andres Bello 890, Barquisimeto', originBranch: 'Sucursal Central', destinationBranch: 'Sucursal Sur', weight: 1.5, dimensions: '25x20x10 cm', declaredValue: 120000, description: 'Ropa y accesorios', status: 'In Transit', createdAt: '2026-05-11', updatedAt: '2026-05-13', qrData: 'AWEN-2026-0006', barcode: '|||AWEN-2026-0006|||' },
  { id: 'ENV-007', guide: 'AWEN-2026-0007', sender: 'Juan Perez', senderId: 'V-78901234', senderPhone: '+58 412 789 0123', recipient: 'Sofia Torres', recipientId: 'V-78901234', recipientPhone: '+58 414 321 0987', recipientAddress: 'Calle 60 123, Merida', originBranch: 'Sucursal Central', destinationBranch: 'Sucursal Occidental', weight: 5.0, dimensions: '40x30x25 cm', declaredValue: 200000, description: 'Equipo deportivo', status: 'Registered', createdAt: '2026-05-13', updatedAt: '2026-05-13', qrData: 'AWEN-2026-0007', barcode: '|||AWEN-2026-0007|||' },
]

export const trackingHistory = {
  'AWEN-2026-0001': [
    { step: 'Registered', date: '2026-05-10', time: '14:30', location: 'Sucursal Central', operator: 'Operador Carlos', completed: true },
    { step: 'Picked Up', date: '2026-05-10', time: '16:00', location: 'Sucursal Central', operator: 'Conductor Pedro', completed: true },
    { step: 'In Transit', date: '2026-05-11', time: '08:00', location: 'Autopista Regional del Centro', operator: 'Conductor Pedro', completed: true },
    { step: 'At Destination Branch', date: '2026-05-12', time: '10:15', location: 'Sucursal Norte', operator: 'Operador Maria', completed: true },
    { step: 'Out for Delivery', date: '2026-05-13', time: '09:00', location: 'Sucursal Norte', operator: 'Conductor Pedro', completed: false },
    { step: 'Delivered', date: null, time: null, location: null, operator: null, completed: false },
  ],
  'AWEN-2026-0002': [
    { step: 'Registered', date: '2026-05-08', time: '10:00', location: 'Sucursal Central', operator: 'Operador Carlos', completed: true },
    { step: 'Picked Up', date: '2026-05-08', time: '11:30', location: 'Sucursal Central', operator: 'Conductor Pedro', completed: true },
    { step: 'In Transit', date: '2026-05-09', time: '07:00', location: 'Autopista Barcelona-Ciudad Guayana', operator: 'Conductor Pedro', completed: true },
    { step: 'At Destination Branch', date: '2026-05-10', time: '14:00', location: 'Sucursal Sur', operator: 'Operador Maria', completed: true },
    { step: 'Out for Delivery', date: '2026-05-11', time: '09:30', location: 'Sucursal Sur', operator: 'Conductor Ana', completed: true },
    { step: 'Delivered', date: '2026-05-12', time: '11:00', location: 'Av. Las Americas 456, Ciudad Guayana', operator: 'Conductor Ana', completed: true },
  ],
}

export const logisticsBatches = [
  { id: 'LOT-001', parcels: ['ENV-001', 'ENV-006'], status: 'Assigned', vehicle: 'ABC-123', driver: 'Conductor Pedro', driverId: 4, parcelCount: 2 },
  { id: 'LOT-002', parcels: ['ENV-003', 'ENV-007'], status: 'Pending Assignment', vehicle: null, driver: null, driverId: null, parcelCount: 2 },
  { id: 'LOT-003', parcels: ['ENV-004'], status: 'Assigned', vehicle: 'XYZ-789', driver: 'Conductor Ana', driverId: 5, parcelCount: 1 },
  { id: 'LOT-004', parcels: [], status: 'Completed', vehicle: 'DEF-456', driver: 'Conductor Pedro', driverId: 4, parcelCount: 3 },
]

export const vehicles = [
  { id: 1, plate: 'ABC-123', model: 'Foton Aumark', capacity: '1500 kg', driver: 'Conductor Pedro' },
  { id: 2, plate: 'XYZ-789', model: 'JMC Carrying', capacity: '1200 kg', driver: 'Conductor Ana' },
  { id: 3, plate: 'DEF-456', model: 'Chevrolet NPR', capacity: '3000 kg', driver: 'Conductor Luis' },
]

export const deliveries = [
  { id: 'DEL-001', guide: 'AWEN-2026-0002', recipient: 'Carmen Flores', driver: 'Conductor Ana', deliveryDate: '2026-05-12', podType: 'Signature', status: 'Completed', signatureData: null, photoUrl: null, gps: '8.3519, -62.6414' },
  { id: 'DEL-002', guide: 'AWEN-2026-0001', recipient: 'Roberto Garcia', driver: 'Conductor Pedro', deliveryDate: null, podType: 'Photo', status: 'Pending', signatureData: null, photoUrl: null, gps: '10.6312, -71.6404' },
  { id: 'DEL-003', guide: 'AWEN-2026-0004', recipient: 'Laura Martinez', driver: 'Conductor Ana', deliveryDate: null, podType: 'Signature', status: 'Pending', signatureData: null, photoUrl: null, gps: '10.2442, -67.5917' },
]

export const dashboardKPIs = {
  totalShipments: 48,
  inTransit: 23,
  delivered: 18,
  returned: 7,
}

export const dailyShipments = [
  { day: 'May 07', count: 5 },
  { day: 'May 08', count: 8 },
  { day: 'May 09', count: 6 },
  { day: 'May 10', count: 10 },
  { day: 'May 11', count: 7 },
  { day: 'May 12', count: 9 },
  { day: 'May 13', count: 3 },
]

export const deliveriesByBranch = [
  { branch: 'Central', count: 18 },
  { branch: 'Norte', count: 8 },
  { branch: 'Sur', count: 10 },
  { branch: 'Este', count: 6 },
  { branch: 'Costa', count: 4 },
  { branch: 'Occidental', count: 2 },
]

export const recentActivity = [
  { time: '09:15', action: 'Encomienda AWEN-2026-0001 asignada a ruta', user: 'Operador Carlos' },
  { time: '08:50', action: 'Conductor Pedro inicia ruta Maracaibo', user: 'Sistema' },
  { time: '08:30', action: 'Nueva encomienda registrada AWEN-2026-0007', user: 'Operador Carlos' },
  { time: '07:45', action: 'Entrega confirmada AWEN-2026-0002', user: 'Conductor Ana' },
  { time: '07:00', action: 'Lote LOT-003 asignado a Conductor Ana', user: 'Operador Maria' },
]

export const reportSummary = {
  totalVolume: 48,
  avgDeliveryTime: '2.4 dias',
  successRate: '72%',
  returnRate: '15%',
}

export const topRoutes = [
  { route: 'Central -> Maracaibo', volume: 12, avgTime: '1.8 dias' },
  { route: 'Central -> Ciudad Guayana', volume: 10, avgTime: '2.1 dias' },
  { route: 'Este -> Maracay', volume: 7, avgTime: '1.5 dias' },
  { route: 'Central -> Barquisimeto', volume: 5, avgTime: '3.5 dias' },
  { route: 'Maracaibo -> Ciudad Guayana', volume: 3, avgTime: '2.8 dias' },
]
