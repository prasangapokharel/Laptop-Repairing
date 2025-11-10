/**
 * User types
 */
export interface User {
  id: number
  username: string
  email: string
  first_name?: string
  last_name?: string
  created_at: string
}

export interface CreateUserRequest {
  username: string
  email: string
  first_name?: string
  last_name?: string
}
