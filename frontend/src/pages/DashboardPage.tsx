import { useNavigate } from 'react-router-dom'
import { logout } from '../features/auth/api'

function DashboardPage() {
  const navigate = useNavigate()

  const handleLogout = async () => {
    try {
      await logout()
      navigate('/login')
    } catch (error) {
      console.error(error)
      navigate('/login')  // 失敗してもログインページに遷移する
    }
  }


  return (
    <div>
      <h1>ダッシュボード</h1>
      <span>今は認証機能のみ</span>
      <button onClick={handleLogout}>ログアウト</button>
    </div>
  )
}

export default DashboardPage
