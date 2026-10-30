export const mockBatches = [
  {
    id: 'LOT-001',
    parcels: ['ENV-001', 'ENV-006'],
    status: 'ASSIGNED',
    vehicle: 'ABC-123',
    driver: 'Conductor Pedro',
    driverId: 4,
    parcelCount: 2
  },
  {
    id: 'LOT-002',
    parcels: ['ENV-003', 'ENV-007'],
    status: 'PENDING',
    vehicle: null,
    driver: null,
    driverId: null,
    parcelCount: 2
  },
  {
    id: 'LOT-003',
    parcels: ['ENV-003', 'ENV-007'],
    status: 'PENDING',
    vehicle: null,
    driver: 'Conductor Ana',
    driverId: 5,
    parcelCount: 2
  }
]

export const mockVehicles = [
  { id: 1, plate: 'ABC-123', model: 'Foton Aumark', capacity: '1500 kg', driver: 'Conductor Pedro' },
  { id: 2, plate: 'XYZ-789', model: 'JMC Carrying', capacity: '1200 kg', driver: 'Conductor Ana' },
  { id: 3, plate: 'DEF-456', model: 'Chevrolet NPR', capacity: '3000 kg', driver: 'Conductor Luis' }
]

export const batchStatuses = ['PENDING', 'ASSIGNED', 'IN_TRANSIT', 'COMPLETED']