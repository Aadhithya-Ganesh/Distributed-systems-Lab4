import { useEffect, useState } from "react";
import "./App.css";

function App() {
  const [items, setItems] = useState([]);
  const [bookings, setBookings] = useState([]);

  const [loadingItems, setLoadingItems] = useState(true);
  const [loadingBookings, setLoadingBookings] = useState(true);
  const [error, setError] = useState(null);

  const [selectedItemId, setSelectedItemId] = useState(null);
  const [selectedQuantity, setSelectedQuantity] = useState(1);
  const [customerName, setCustomerName] = useState("");
  const [successMessage, setSuccessMessage] = useState("");

  // ---- FETCH ITEMS ----
  useEffect(() => {
    const fetchItems = async () => {
      try {
        setLoadingItems(true);
        const response = await fetch(`/api/items/`, {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        });

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        console.log("items:", data);
        setItems(data);
      } catch (err) {
        setError(err.message);
        console.error("Failed to fetch items:", err);
      } finally {
        setLoadingItems(false);
      }
    };

    fetchItems();
  }, []);

  // ---- FETCH BOOKINGS ----
  useEffect(() => {
    const fetchBookings = async () => {
      try {
        setLoadingBookings(true);
        const response = await fetch(`/api/booking/`, {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        });

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        console.log("bookings:", data);
        setBookings(data);
      } catch (err) {
        setError(err.message);
        console.error("Failed to fetch bookings:", err);
      } finally {
        setLoadingBookings(false);
      }
    };

    fetchBookings();
  }, []); // <-- fetch bookings once on mount

  const handleSubmit = async (event) => {
    event.preventDefault();
    setSuccessMessage("");
    setError(null);

    if (!selectedItemId) {
      setError("Please select an item.");
      return;
    }

    if (!customerName.trim()) {
      setError("Please enter your name.");
      return;
    }

    try {
      const response = await fetch(`/api/booking/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          customer_name: customerName,
          item_id: selectedItemId,
          quantity: selectedQuantity,
          status: "PENDING",
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      console.log("Booking created:", data);
      setSuccessMessage(
        `Booking created for ${data.customer_name} (item #${data.item_id}, qty ${data.quantity}).`
      );

      // append new booking to table
      setBookings((prev) => [...prev, data]);
    } catch (err) {
      setError(err.message);
      console.error("Failed to create booking:", err);
    }
  };

  if (loadingItems) {
    return <div>Loading items...</div>;
  }

  return (
    <div>
      <h1>Items List</h1>

      <form onSubmit={handleSubmit}>
        <table border="1" style={{ borderCollapse: "collapse", width: "100%" }}>
          <thead>
            <tr>
              <th>Select</th>
              <th>Name</th>
              <th>Description</th>
              <th>Price</th>
              <th>Available</th>
              <th>Choose quantity</th>
            </tr>
          </thead>
          <tbody>
            {items.map((item) => {
              const isSelected = selectedItemId === item.id;

              return (
                <tr key={item.id}>
                  <td>
                    <input
                      type="radio"
                      name="selectedItem"
                      value={item.id}
                      checked={isSelected}
                      onChange={() => {
                        setSelectedItemId(item.id);
                        setSelectedQuantity(1);
                      }}
                    />
                  </td>
                  <td>{item.name}</td>
                  <td>{item.description}</td>
                  <td>${item.price}</td>
                  <td>{item.quantity}</td>
                  <td>
                    <select
                      disabled={!isSelected}
                      value={isSelected ? selectedQuantity : 1}
                      onChange={(e) =>
                        setSelectedQuantity(Number(e.target.value))
                      }
                    >
                      {Array.from(
                        { length: item.quantity },
                        (_, i) => i + 1
                      ).map((q) => (
                        <option key={q} value={q}>
                          {q}
                        </option>
                      ))}
                    </select>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>

        {items.length === 0 && <div>No items found</div>}

        <div style={{ marginTop: "1rem" }}>
          <h2>Purchase</h2>
          <label>
            Customer name:{" "}
            <input
              type="text"
              value={customerName}
              onChange={(e) => setCustomerName(e.target.value)}
            />
          </label>
        </div>

        <button type="submit" style={{ marginTop: "1rem" }}>
          Submit booking
        </button>
      </form>

      {successMessage && (
        <div style={{ marginTop: "1rem", color: "green" }}>
          {successMessage}
        </div>
      )}
      {error && (
        <div style={{ marginTop: "1rem", color: "red" }}>Error: {error}</div>
      )}

      <h2 style={{ marginTop: "2rem" }}>Bookings</h2>

      {loadingBookings ? (
        <div>Loading bookings...</div>
      ) : bookings.length === 0 ? (
        <div>No bookings yet</div>
      ) : (
        <table
          border="1"
          style={{
            borderCollapse: "collapse",
            width: "100%",
            marginTop: "0.5rem",
          }}
        >
          <thead>
            <tr>
              <th>ID</th>
              <th>Customer Name</th>
              <th>Item ID</th>
              <th>Quantity</th>
              <th>Total Price</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {bookings.map((booking) => (
              <tr key={booking.id}>
                <td>{booking.id}</td>
                <td>{booking.customer_name}</td>
                <td>{booking.item_id}</td>
                <td>{booking.quantity}</td>
                <td>{booking.total_price}</td>
                <td>{booking.status}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default App;
