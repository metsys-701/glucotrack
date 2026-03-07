import {
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
  Tooltip,
  Legend,
  Chart as ChartJS
} from "chart.js"

import annotationPlugin from "chartjs-plugin-annotation"
import { Line } from "react-chartjs-2"

ChartJS.register(
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
  Tooltip,
  Legend,
  annotationPlugin
)

function GlucoseChart({ records }) {

  if (!records || records.length === 0) {
    return <p>No glucose data</p>
  }

  // Kayıtları zaman sırasına göre sırala
  const sorted = [...records].sort(
    (a, b) => new Date(a.created_at) - new Date(b.created_at)
  )

  // Grafik label (saat)
  const labels = sorted.map((r) =>
    new Date(r.created_at).toLocaleTimeString()
  )

  const values = sorted.map((r) => r.glucose_value)

  const data = {
    labels,
    datasets: [
      {
        label: "Glucose",
        data: values,
        borderColor: "#3b82f6",
        backgroundColor: "#93c5fd",
        tension: 0.4,
        pointRadius: 4
      }
    ]
  }

  const options = {

    responsive: true,

    plugins: {

      legend: {
        display: false
      },

      annotation: {

        annotations: {

          lowLine: {
            type: "line",
            yMin: 70,
            yMax: 70,
            borderColor: "orange",
            borderWidth: 2,
            label: {
              content: "Low (70)",
              enabled: true,
              position: "end"
            }
          },

          targetLine: {
            type: "line",
            yMin: 140,
            yMax: 140,
            borderColor: "green",
            borderWidth: 2,
            label: {
              content: "Target (140)",
              enabled: true,
              position: "end"
            }
          },

          highLine: {
            type: "line",
            yMin: 180,
            yMax: 180,
            borderColor: "red",
            borderWidth: 2,
            label: {
              content: "High (180)",
              enabled: true,
              position: "end"
            }
          }

        }
      }

    },

    scales: {
      y: {
        beginAtZero: false
      }
    }

  }

  return (

    <div className="bg-white p-6 rounded-xl shadow">

      <h2 className="text-xl font-semibold mb-4">
        Glucose Trend
      </h2>

      <Line data={data} options={options} />

    </div>

  )

}

export default GlucoseChart