import { useEffect, useState } from "react"
import { getDashboard } from "../services/api"
import DashboardCard from "../components/DashboardCard"

function Dashboard({ token }) {

  const [stats, setStats] = useState(null)

  useEffect(() => {

    const loadData = async () => {

      const data = await getDashboard(token)

      setStats(data)

    }

    loadData()

  }, [token])

  if (!stats) {
    return <p>Loading...</p>
  }

  return (

    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">

      <DashboardCard
        title="Today Avg"
        value={stats.today_avg}
        unit="mg/dL"
      />

      <DashboardCard
        title="Last Measurement"
        value={stats.last_measurement}
        unit="mg/dL"
      />

      <DashboardCard
        title="Time in Range"
        value={stats.time_in_range}
        unit="%"
      />

      <DashboardCard
        title="Tight Control"
        value={stats.tight_range}
        unit="%"
      />

    </div>

  )
}

export default Dashboard