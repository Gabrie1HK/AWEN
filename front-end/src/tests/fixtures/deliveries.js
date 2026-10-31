export const mockDeliveries = [
  {
    id: 'DEL-001',
    guide: 'AWEN-2026-0002',
    recipient: 'Carmen Flores',
    driver: 'Conductor Ana',
    deliveryDate: '2026-05-12',
    podType: 'SIGNATURE',
    status: 'COMPLETED',
    signatureData: null,
    photoUrl: null,
    gps: '8.3519, -62.6414'
  },
  {
    id: 'DEL-002',
    guide: 'AWEN-2026-0001',
    recipient: 'Roberto Garcia',
    driver: 'Conductor Pedro',
    deliveryDate: null,
    podType: 'PHOTO',
    status: 'PENDING',
    signatureData: null,
    photoUrl: null,
    gps: '10.6312, -71.6404'
  }
]

export const podTypes = ['PHOTO', 'SIGNATURE', 'BOTH']
export const deliveryStatuses = ['PENDING', 'IN_PROGRESS', 'COMPLETED', 'FAILED']