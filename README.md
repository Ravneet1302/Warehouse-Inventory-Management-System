<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Warehouse Inventory</title>
    <link
      rel="stylesheet"
      href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css"
    />
  </head>
  <body>
    <div class="container mt-5">
      <h2 class="text-center mb-4">Warehouse Inventory Management</h2>

    
      <div class="card p-4 shadow">
        <h4 class="mb-3">Set Storage Capacity</h4>
        {% if max_capacity %}
        <p class="text-muted">Current capacity: {{ max_capacity }}</p>
        {% endif %}

        <form action="/set_capacity" method="POST">
          <div class="mb-3">
            <label class="form-label">Warehouse Capacity:</label>
            <input
              type="number"
              class="form-control"
              name="max_capacity"
              required
              min="1"
            />
          </div>
          <button type="submit" class="btn btn-primary">Set Capacity</button>
        </form>
      </div>

     
      <div class="card p-4 shadow mt-4">
        <h4 class="mb-3">Add New Item</h4>
        <form action="/add_item" method="POST">
          <div class="mb-3">
            <label class="form-label">Item Name:</label>
            <input type="text" class="form-control" name="item_name" required />
          </div>
          <div class="mb-3">
            <label class="form-label">Space:</label>
            <input
              type="number"
              class="form-control"
              name="value"
              required
              min="1"
            />
          </div>
          <div class="mb-3">
            <label class="form-label">Profit:</label>
            <input
              type="number"
              class="form-control"
              name="weight"
              required
              min="1"
            />
          </div>
          <button type="submit" class="btn btn-success">Add Item</button>
        </form>
      </div>

      
      <div class="mt-4">
        <h4>Current Inventory</h4>
        {% if inventory %}
        <table class="table table-striped">
          <thead class="table-dark">
            <tr>
              <th>#</th>
              <th>Item Name</th>
              <th>Space</th>
              <th>Profit</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {% for item in inventory %}
            <tr>
              <td>{{ loop.index }}</td>
              <td>{{ item.name }}</td>
              <td>{{ item.value }}</td>
              <td>{{ item.weight }}</td>

              <td>
                <a href="/edit/{{ item.id }}" class="btn btn-warning btn-sm"
                  >Edit</a
                >
                <a
                  href="/delete/{{ item.id }}"
                  class="btn btn-danger btn-sm"
                  onclick="return confirm('Are you sure you want to delete this item?')"
                >
                  Delete
                </a>
              </td>
            </tr>
            {% endfor %}
          </tbody>
        </table>
        {% else %}
        <p class="text-muted">No items in inventory yet.</p>
        {% endif %}
      </div>

     
      <div class="text-center mt-4">
        <!-- <form action="/knapsack" method="POST"> -->
        <form action="/calculate_knapsack" method="POST">
          <button type="submit" class="btn btn-primary">
            Calculate Knapsack
          </button>
        </form>
      </div>

      <!-- Knapsack Results -->
      {% if selected_items %}
      <div class="card p-4 shadow mt-4">
        <h4>Optimal Storage Selection</h4>
        <p><strong>Total Profit:</strong> {{ total_profit }}</p>
        <ul>
          {% for item in selected_items %}
          <li>
            {{ item.name }} - Stored: {{ item.weight|round(2) }} units
            (Fraction: {{ item.fraction|round(2) }})
          </li>
          {% endfor %}
        </ul>
        <img
          src="{{ url_for('static', filename='storage_chart.png') }}"
          alt="Storage Allocation"
          class="img-fluid mt-3"
        />
      </div>
      {% endif %}
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
  </body>
</html>
