export const mockUsers = {
  admin: {
    id: 1,
    name: 'Admin',
    last_name: 'Principal',
    ci: 'V-12345678',
    email: 'admin@awen.com',
    role: 'Admin',
    branch: 'Sucursal Central',
    phone: '+58 212 212 3456',
    active: true,
    lastLogin: '2026-05-12 09:30',
    avatar: null
  },
  operator: {
    id: 2,
    name: 'Carlos',
    last_name: 'Operador',
    ci: 'V-23456789',
    email: 'operador.carlos@awen.com',
    role: 'Warehouse Operator',
    branch: 'Sucursal Central',
    phone: '+58 412 123 4567',
    active: true,
    lastLogin: '2026-05-13 07:15',
    avatar: null
  },
  driver: {
    id: 4,
    name: 'Pedro',
    last_name: 'Conductor',
    ci: 'V-34567890',
    email: 'conductor.pedro@awen.com',
    role: 'Driver',
    branch: 'Sucursal Central',
    phone: '+58 414 987 6543',
    active: true,
    lastLogin: '2026-05-13 06:00',
    avatar: null
  },
  client: {
    id: 6,
    name: 'Juan',
    last_name: 'Cliente',
    ci: 'V-67890123',
    email: 'juan@email.com',
    role: 'Client',
    branch: null,
    phone: '+58 412 789 0123',
    address: 'Calle 60 123, Merida',
    active: true,
    lastLogin: '2026-05-10 14:00',
    avatar: null
  }
}

export const mockTokens = {
  admin: 'admin-token-123',
  operator: 'operator-token-123',
  driver: 'driver-token-123',
  client: 'client-token-123'
}