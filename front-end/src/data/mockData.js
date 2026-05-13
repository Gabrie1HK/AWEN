export const branches = [
  { id: 1, name: 'Sucursal Central', city: 'Santiago', address: 'Av. Libertador 1234', manager: 'Carlos Muñoz', phone: '+56 2 2123 4567', active: true },
  { id: 2, name: 'Sucursal Norte', city: 'Antofagasta', address: 'Calle Comercio 567', manager: 'María Soto', phone: '+56 55 2123 4567', active: true },
  { id: 3, name: 'Sucursal Sur', city: 'Concepción', address: 'Av. Los Carrera 890', manager: 'Pedro Torres', phone: '+56 41 2123 4567', active: true },
  { id: 4, name: 'Sucursal Este', city: 'Providencia', address: 'Av. Providencia 2345', manager: 'Ana López', phone: '+56 2 2345 6789', active: true },
  { id: 5, name: 'Sucursal Costa', city: 'Valparaíso', address: 'Av. Errázuriz 678', manager: 'José Rivas', phone: '+56 32 2123 4567', active: false },
  { id: 6, name: 'Sucursal Austral', city: 'Punta Arenas', address: 'Av. Colón 901', manager: 'Luis Vargas', phone: '+56 61 2123 4567', active: true },
]

export const users = [
  { id: 1, name: 'Admin Principal', email: 'admin@awen.cl', role: 'Admin', branch: 'Sucursal Central', active: true, lastLogin: '2026-05-12 09:30' },
  { id: 2, name: 'Operador Carlos', email: 'operador.carlos@awen.cl', role: 'Warehouse Operator', branch: 'Sucursal Central', active: true, lastLogin: '2026-05-13 07:15' },
  { id: 3, name: 'Operador María', email: 'operador.maria@awen.cl', role: 'Warehouse Operator', branch: 'Sucursal Norte', active: true, lastLogin: '2026-05-12 22:40' },
  { id: 4, name: 'Conductor Pedro', email: 'conductor.pedro@awen.cl', role: 'Driver', branch: 'Sucursal Central', active: true, lastLogin: '2026-05-13 06:00' },
  { id: 5, name: 'Conductor Ana', email: 'conductor.ana@awen.cl', role: 'Driver', branch: 'Sucursal Sur', active: true, lastLogin: '2026-05-12 18:20' },
  { id: 6, name: 'Cliente Juan', email: 'juan@email.com', role: 'Client', branch: '-', active: true, lastLogin: '2026-05-10 14:00' },
  { id: 7, name: 'Cliente Marta', email: 'marta@email.com', role: 'Client', branch: '-', active: false, lastLogin: '2026-04-28 11:30' },
]

export const parcels = [
  { id: 'ENV-001', guide: 'AWEN-2026-0001', sender: 'TechStore SpA', senderId: '76.123.456-7', senderPhone: '+56 9 1234 5678', recipient: 'Roberto García', recipientId: '12.345.678-9', recipientPhone: '+56 9 9876 5432', recipientAddress: 'Av. Siempre Viva 742, Santiago', originBranch: 'Sucursal Central', destinationBranch: 'Sucursal Norte', weight: 2.5, dimensions: '30x20x15 cm', declaredValue: 150000, description: 'Notebook y accesorios', status: 'In Transit', createdAt: '2026-05-10', updatedAt: '2026-05-13', qrData: 'AWEN-2026-0001', barcode: '|||AWEN-2026-0001|||' },
  { id: 'ENV-002', guide: 'AWEN-2026-0002', sender: 'Distribuidora Sur Ltda', senderId: '77.987.654-3', senderPhone: '+56 9 2345 6789', recipient: 'Carmen Flores', recipientId: '23.456.789-0', recipientPhone: '+56 9 8765 4321', recipientAddress: 'Los Pinos 456, Concepción', originBranch: 'Sucursal Central', destinationBranch: 'Sucursal Sur', weight: 15.0, dimensions: '50x40x30 cm', declaredValue: 450000, description: 'Equipo de sonido profesional', status: 'Delivered', createdAt: '2026-05-08', updatedAt: '2026-05-12', qrData: 'AWEN-2026-0002', barcode: '|||AWEN-2026-0002|||' },
  { id: 'ENV-003', guide: 'AWEN-2026-0003', sender: 'Farmacias del Centro', senderId: '76.789.012-3', senderPhone: '+56 9 3456 7890', recipient: 'Dr. Andrés Vega', recipientId: '34.567.890-1', recipientPhone: '+56 9 7654 3210', recipientAddress: 'O\u2019Higgins 789, Rancagua', originBranch: 'Sucursal Central', destinationBranch: 'Sucursal Central', weight: 0.8, dimensions: '20x15x10 cm', declaredValue: 80000, description: 'Medicamentos controlados', status: 'Registered', createdAt: '2026-05-13', updatedAt: '2026-05-13', qrData: 'AWEN-2026-0003', barcode: '|||AWEN-2026-0003|||' },
  { id: 'ENV-004', guide: 'AWEN-2026-0004', sender: 'ElectroHogar SA', senderId: '76.456.789-0', senderPhone: '+56 9 4567 8901', recipient: 'Laura Martínez', recipientId: '45.678.901-2', recipientPhone: '+56 9 6543 2109', recipientAddress: 'Bellavista 234, Valparaíso', originBranch: 'Sucursal Este', destinationBranch: 'Sucursal Costa', weight: 8.0, dimensions: '60x40x35 cm', declaredValue: 320000, description: 'Aspiradora robot', status: 'At Destination Branch', createdAt: '2026-05-09', updatedAt: '2026-05-13', qrData: 'AWEN-2026-0004', barcode: '|||AWEN-2026-0004|||' },
  { id: 'ENV-005', guide: 'AWEN-2026-0005', sender: 'Librería Nacional', senderId: '77.234.567-8', senderPhone: '+56 9 5678 9012', recipient: 'Patricio Silva', recipientId: '56.789.012-3', recipientPhone: '+56 9 5432 1098', recipientAddress: 'Comercio 567, Antofagasta', originBranch: 'Sucursal Central', destinationBranch: 'Sucursal Norte', weight: 3.2, dimensions: '35x25x20 cm', declaredValue: 45000, description: 'Libros y material educativo', status: 'Returned', createdAt: '2026-05-05', updatedAt: '2026-05-11', qrData: 'AWEN-2026-0005', barcode: '|||AWEN-2026-0005|||' },
  { id: 'ENV-006', guide: 'AWEN-2026-0006', sender: 'Moda Urbana SpA', senderId: '76.567.890-1', senderPhone: '+56 9 6789 0123', recipient: 'Daniela Rojas', recipientId: '67.890.123-4', recipientPhone: '+56 9 4321 0987', recipientAddress: 'Los Alerces 890, Puerto Montt', originBranch: 'Sucursal Central', destinationBranch: 'Sucursal Sur', weight: 1.5, dimensions: '25x20x10 cm', declaredValue: 120000, description: 'Ropa y accesorios', status: 'In Transit', createdAt: '2026-05-11', updatedAt: '2026-05-13', qrData: 'AWEN-2026-0006', barcode: '|||AWEN-2026-0006|||' },
  { id: 'ENV-007', guide: 'AWEN-2026-0007', sender: 'Juan Pérez', senderId: '78.901.234-5', senderPhone: '+56 9 7890 1234', recipient: 'Sofía Torres', recipientId: '78.901.234-5', recipientPhone: '+56 9 3210 9876', recipientAddress: 'Calle Larga 123, Punta Arenas', originBranch: 'Sucursal Central', destinationBranch: 'Sucursal Austral', weight: 5.0, dimensions: '40x30x25 cm', declaredValue: 200000, description: 'Equipo deportivo', status: 'Registered', createdAt: '2026-05-13', updatedAt: '2026-05-13', qrData: 'AWEN-2026-0007', barcode: '|||AWEN-2026-0007|||' },
]

export const trackingHistory = {
  'AWEN-2026-0001': [
    { step: 'Registered', date: '2026-05-10', time: '14:30', location: 'Sucursal Central', operator: 'Operador Carlos', completed: true },
    { step: 'Picked Up', date: '2026-05-10', time: '16:00', location: 'Sucursal Central', operator: 'Conductor Pedro', completed: true },
    { step: 'In Transit', date: '2026-05-11', time: '08:00', location: 'Ruta 5 Norte', operator: 'Conductor Pedro', completed: true },
    { step: 'At Destination Branch', date: '2026-05-12', time: '10:15', location: 'Sucursal Norte', operator: 'Operador María', completed: true },
    { step: 'Out for Delivery', date: '2026-05-13', time: '09:00', location: 'Sucursal Norte', operator: 'Conductor Pedro', completed: false },
    { step: 'Delivered', date: null, time: null, location: null, operator: null, completed: false },
  ],
  'AWEN-2026-0002': [
    { step: 'Registered', date: '2026-05-08', time: '10:00', location: 'Sucursal Central', operator: 'Operador Carlos', completed: true },
    { step: 'Picked Up', date: '2026-05-08', time: '11:30', location: 'Sucursal Central', operator: 'Conductor Pedro', completed: true },
    { step: 'In Transit', date: '2026-05-09', time: '07:00', location: 'Ruta 5 Sur', operator: 'Conductor Pedro', completed: true },
    { step: 'At Destination Branch', date: '2026-05-10', time: '14:00', location: 'Sucursal Sur', operator: 'Operador María', completed: true },
    { step: 'Out for Delivery', date: '2026-05-11', time: '09:30', location: 'Sucursal Sur', operator: 'Conductor Ana', completed: true },
    { step: 'Delivered', date: '2026-05-12', time: '11:00', location: 'Los Pinos 456, Concepción', operator: 'Conductor Ana', completed: true },
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
  { id: 'DEL-001', guide: 'AWEN-2026-0002', recipient: 'Carmen Flores', driver: 'Conductor Ana', deliveryDate: '2026-05-12', podType: 'Signature', status: 'Completed', signatureData: null, photoUrl: null, gps: '-36.8269, -73.0499' },
  { id: 'DEL-002', guide: 'AWEN-2026-0001', recipient: 'Roberto García', driver: 'Conductor Pedro', deliveryDate: null, podType: 'Photo', status: 'Pending', signatureData: null, photoUrl: null, gps: '-23.6509, -70.3975' },
  { id: 'DEL-003', guide: 'AWEN-2026-0004', recipient: 'Laura Martínez', driver: 'Conductor Ana', deliveryDate: null, podType: 'Signature', status: 'Pending', signatureData: null, photoUrl: null, gps: '-33.0472, -71.6127' },
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
  { branch: 'Austral', count: 2 },
]

export const recentActivity = [
  { time: '09:15', action: 'Encomienda AWEN-2026-0001 asignada a ruta', user: 'Operador Carlos' },
  { time: '08:50', action: 'Conductor Pedro inicia ruta Norte', user: 'Sistema' },
  { time: '08:30', action: 'Nueva encomienda registrada AWEN-2026-0007', user: 'Operador Carlos' },
  { time: '07:45', action: 'Entrega confirmada AWEN-2026-0002', user: 'Conductor Ana' },
  { time: '07:00', action: 'Lote LOT-003 asignado a Conductor Ana', user: 'Operador María' },
]

export const reportSummary = {
  totalVolume: 48,
  avgDeliveryTime: '2.4 días',
  successRate: '72%',
  returnRate: '15%',
}

export const topRoutes = [
  { route: 'Central → Norte', volume: 12, avgTime: '1.8 días' },
  { route: 'Central → Sur', volume: 10, avgTime: '2.1 días' },
  { route: 'Este → Costa', volume: 7, avgTime: '1.5 días' },
  { route: 'Central → Austral', volume: 5, avgTime: '3.5 días' },
  { route: 'Norte → Sur', volume: 3, avgTime: '2.8 días' },
]
