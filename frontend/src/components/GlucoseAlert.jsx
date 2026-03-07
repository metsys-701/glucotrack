function GlucoseAlert({ value }) {

  if (!value) return null

  let message = ""
  let color = ""

  if (value < 70) {
    message = "⚠ Hypoglycemia risk"
    color = "bg-red-100 text-red-700"
  }

  else if (value <= 140) {
    message = "✓ Excellent glucose level"
    color = "bg-green-100 text-green-700"
  }

  else if (value <= 180) {
    message = "⚠ Slightly elevated glucose"
    color = "bg-yellow-100 text-yellow-700"
  }

  else {
    message = "⚠ Hyperglycemia detected"
    color = "bg-red-100 text-red-700"
  }

  return (

    <div className={`p-4 rounded-lg mb-6 ${color}`}>

      <p className="font-semibold">
        Last glucose: {value} mg/dL
      </p>

      <p className="text-sm">
        {message}
      </p>

    </div>

  )
}

export default GlucoseAlert