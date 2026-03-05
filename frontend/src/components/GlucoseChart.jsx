import {
  Chart as ChartJS,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
  Tooltip,
  Legend
} from "chart.js"

import { Line } from "react-chartjs-2"

ChartJS.register(
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
  Tooltip,
  Legend
)

function GlucoseChart({ records }) {

  const labels = records.map(r =>
    new Date(r.created_at).toLocaleDateString()
  )

  const values = records.map(r => r.glucose_value)

  const data = {
    labels,
    datasets: [
      {
        label: "Glucose mg/dL",
        data: values,
        borderColor: "#2563eb",
        backgroundColor: "#60a5fa",
        tension: 0.3
      }
    ]
  }

  const options = {
    responsive: true,
    plugins: {
      legend: {
        display: false
      }
    },
    scales: {
      y: {
        min: 60,
        max: 200
      }
    }
  }

  return (
    <div className="bg-white rounded-xl shadow p-6 mt-10">
      <h2 className="text-xl font-semibold mb-4">
        Glucose Trend
      </h2>

      <Line data={data} options={options} />
    </div>
  )
}

export default GlucoseChart