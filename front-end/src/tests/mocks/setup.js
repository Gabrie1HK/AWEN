import { beforeAll, afterEach, afterAll } from 'vitest'
import { setupServer } from 'msw/node'
import { handlers } from './handlers'

// Servidor MSW para tests de integracion. Se importa solo en los suites que lo usan,
// para no interceptar los fetch que otros tests sustituyen con vi.fn().
export const server = setupServer(...handlers)

beforeAll(() => server.listen({ onUnhandledRequest: 'error' }))

afterEach(() => server.resetHandlers())

afterAll(() => server.close())
