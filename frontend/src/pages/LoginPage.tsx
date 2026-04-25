import { useNavigate } from 'react-router-dom'
import LoginForm from '../features/auth/LoginForm'
import type { LoginRequest } from '../features/auth/types'
import { login } from '../features/auth/api'

function LoginPage() {
  const navigate = useNavigate()

  const handleSubmit = async (data: LoginRequest) => {
    try {
      await login(data)
      navigate('/')
    } catch (error) {
      console.error(error)
    }
  }

  return (
    <div>
      <h1>ログイン</h1>
      <LoginForm onSubmit={handleSubmit} />
    </div>
  )
}

export default LoginPage
