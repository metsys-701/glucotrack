function DashboardCard({ title, value, unit }) {

  return (

    <div className="bg-white shadow-lg rounded-xl p-5">

      <p className="text-gray-500 text-sm">
        {title}
      </p>

      <p className="text-3xl font-bold mt-2">
        {value ?? "--"} {unit}
      </p>

    </div>

  )
}

export default DashboardCard