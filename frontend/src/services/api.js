const API_URL = "http://127.0.0.1:8000"

export const loginUser = async (email, password) => {

  const response = await fetch(`${API_URL}/auth/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: new URLSearchParams({
      username: email,
      password: password,
    }),
  })

  const data = await response.json()

  if (!response.ok) {
    throw new Error(data.detail || "Login failed")
  }

  return data
}

export const getDashboard = async (token) => {

  const response = await fetch(`${API_URL}/glucose/dashboard`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })

  return response.json()
}

export const getGlucose = async (token) => {

  const response = await fetch(`${API_URL}/glucose?skip=0&limit=10`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })

  return response.json()
}