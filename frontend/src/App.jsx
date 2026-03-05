import { useEffect, useState } from "react"
import GlucoseChart from "./components/GlucoseChart"

function App() {

  const [stats, setStats] = useState(null)
  const [records, setRecords] = useState([])

  const token = localStorage.getItem("token")

  useEffect(() => {

    fetchDashboard()
    fetchRecords()

  }, [])



  const fetchDashboard = async () => {

    const response = await fetch("http://127.0.0.1:8000/glucose/dashboard", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })

    const data = await response.json()

    setStats(data)

  }



  const fetchRecords = async () => {

    const response = await fetch(
      "http://127.0.0.1:8000/glucose/?skip=0&limit=5",
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    )

    const data = await response.json()

    setRecords(data.data || [])

  }



  return (

    <div className="min-h-screen bg-gray-100 p-10">

      <h1 className="text-4xl font-bold mb-8">
        GlucoTrack Dashboard
      </h1>

      {!stats ? (

        <p>Loading...</p>

      ) : (

        <div>

          {/* Dashboard Cards */}

          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-10">

            <Card
              title="Today Avg"
              value={stats.today_avg}
              unit="mg/dL"
            />

            <Card
              title="Last Measurement"
              value={stats.last_measurement}
              unit="mg/dL"
            />

            <Card
              title="Time in Range"
              value={stats.time_in_range}
              unit="%"
            />

            <Card
              title="Tight Control"
              value={stats.tight_range}
              unit="%"
            />

          </div>



          {/* Recent Records */}


          <div className="bg-white rounded-xl shadow p-6">

            <h2 className="text-xl font-semibold mb-4">
              Recent Glucose Records
            </h2>

            {records.length === 0 ? (

              <p>No records found</p>

            ) : (

              <ul>

                {records.map((r) => (

                  <li
                    key={r.id}
                    className="flex justify-between border-b py-2"
                  >
                    <span>{r.glucose_value} mg/dL</span>
                    <span className="text-gray-500">{r.note}</span>
                  </li>

                ))}

              </ul>

            )}

          </div>
          
          <GlucoseChart records={records} />

        </div>

      )}

    </div>

  )

}



function Card({ title, value, unit }) {

  return (

    <div className="bg-white rounded-xl shadow p-6">

      <p className="text-gray-500 text-sm">
        {title}
      </p>

      <p className="text-3xl font-bold mt-2">

        {value ?? "--"} {unit}

      </p>

    </div>

  )

}

export default App