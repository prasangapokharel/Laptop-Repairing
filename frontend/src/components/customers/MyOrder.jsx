import React, { useState, useMemo, useEffect } from "react";

// Sample data for the orders table
const INITIAL_ORDERS = [
  {
    id: "001",
    customer: "John Doe",
    device: "Dell XPS 13",
    issue: "Screen flickering",
    date: "2024-04-01",
    status: "Pending",
  },
  {
    id: "002",
    customer: "Jane Smith",
    device: "MacBook Pro",
    issue: "Battery issue",
    date: "2024-04-02",
    status: "Repairing",
  },
  {
    id: "003",
    customer: "Bob Johnson",
    device: "Lenovo",
    issue: "Hard drive failure",
    date: "2024-04-03",
    status: "Completed",
  },
  {
    id: "004",
    customer: "Alice Brown",
    device: "Surface Pro",
    issue: "Software update error",
    date: "2024-04-04",
    status: "Cancelled",
  },
  {
    id: "005",
    customer: "Charlie Davis",
    device: "HP Envy",
    issue: "Overheating",
    date: "2024-04-05",
    status: "Pending",
  },
  {
    id: "006",
    customer: "Eva Green",
    device: 'iMac 27"',
    issue: "Display calibration",
    date: "2024-04-06",
    status: "Repairing",
  },
];

// Status configuration for colors and display text
const STATUS_CONFIG = {
  Pending: { color: "bg-yellow-500", label: "Pending" },
  Repairing: { color: "bg-blue-500", label: "Repairing" },
  Completed: { color: "bg-green-500", label: "Completed" },
  Cancelled: { color: "bg-red-500", label: "Cancelled" },
};

// --- Custom Components ---

/**
 * Renders a colored status indicator dot and the status text.
 */
const StatusIndicator = ({ status }) => {
  const config = STATUS_CONFIG[status] || {
    color: "bg-gray-400",
    label: status,
  };
  return (
    <div className="flex items-center space-x-2">
      <span className={`w-3 h-3 rounded-full ${config.color}`}></span>
      <span className="hidden lg:inline text-sm font-medium text-gray-700">
        {config.label}
      </span>
    </div>
  );
};

/**
 * Renders the filter buttons for the different order statuses.
 */
const FilterButtons = ({ activeFilter, setActiveFilter }) => {
  const statusKeys = ["Pending", "Repairing", "Completed", "Cancelled"];

  const getButtonClasses = (status) => {
    const base =
      "px-4 py-2 font-semibold text-white rounded-xl transition-all duration-200 shadow-md transform hover:scale-[1.02] focus:outline-none focus:ring-4";
    const config = STATUS_CONFIG[status];
    const isActive = activeFilter === status;

    if (isActive) {
      // Active state: Brighter background, strong shadow
      return `${base} ${config.color} shadow-lg shadow-gray-500/50`;
    } else {
      // Inactive state: Subtle background, slightly less shadow, brighter hover
      return `${base} ${config.color.replace("-500", "-400")} hover:${
        config.color
      } opacity-80 hover:opacity-100`;
    }
  };

  return (
    <div className="flex flex-wrap gap-2 md:gap-4">
      {statusKeys.map((status) => (
        <button
          style={{ color: "black" }}
          key={status}
          onClick={() => setActiveFilter(status)}
          className={getButtonClasses(status)}>
          {status}
        </button>
      ))}
    </div>
  );
};

// Moved out of MyOrder to avoid nested-component warnings
const TableHeader = () => (
  <div className="hidden lg:grid grid-cols-7 gap-4 py-3 px-4 border-b text-left text-sm font-semibold text-gray-700 bg-gray-100/50 rounded-t-xl">
    <div className="col-span-1">Order ID</div>
    <div className="col-span-1">Customer</div>
    <div className="col-span-1">Device</div>
    <div className="col-span-1">Issue</div>
    <div className="col-span-1">Date</div>
    <div className="col-span-1">Status</div>
    <div className="col-span-1">Actions</div>
  </div>
);

/**
 * Main application component.
 */
const MyOrder = () => {
  const [activeFilter, setActiveFilter] = useState("Pending"); // Start on Pending tab
  const [selectedDropdownStatus, setSelectedDropdownStatus] = useState("All");
  const [isMobileView, setIsMobileView] = useState(false);

  // Effect to check screen size for responsive rendering
  useEffect(() => {
    const checkMobile = () => {
      setIsMobileView(window.innerWidth < 1024); // Tailwind's lg breakpoint
    };
    checkMobile();
    window.addEventListener("resize", checkMobile);
    return () => window.removeEventListener("resize", checkMobile);
  }, []);

  // Determine the status filter based on view (Buttons for Desktop, Dropdown for Mobile)
  const currentFilter = isMobileView ? selectedDropdownStatus : activeFilter;

  // Filter the orders based on the current filter state
  const filteredOrders = useMemo(() => {
    if (currentFilter === "All") {
      return INITIAL_ORDERS;
    }
    return INITIAL_ORDERS.filter((order) => order.status === currentFilter);
  }, [currentFilter]);

  // Handle "View" action (for demonstration)
  const handleView = (id) => {
    // In a real app, this would open a modal or navigate to a detail page
    console.log(`Viewing order details for ID: ${id}`);
  };

  // --- Table Components ---

  const TableRow = ({ order, isLast }) => (
    // Desktop Row (Grid)
    <div
      className={`hidden lg:grid grid-cols-7 gap-4 py-4 px-4 text-sm border-b ${
        !isLast ? "border-gray-200" : "border-b-0"
      }`}>
      <div className="col-span-1 font-medium text-gray-800">{order.id}</div>
      <div className="col-span-1 text-gray-600">{order.customer}</div>
      <div className="col-span-1 text-gray-600">{order.device}</div>
      <div className="col-span-1 text-gray-600">{order.issue}</div>
      <div className="col-span-1 text-gray-600">{order.date}</div>
      <div className="col-span-1">
        <StatusIndicator status={order.status} />
      </div>
      <div className="col-span-1">
        <button
          onClick={() => handleView(order.id)}
          className="px-3 py-1 bg-blue-600 text-white text-xs font-semibold rounded-lg shadow-md hover:bg-blue-700 transition-colors duration-200">
          view
        </button>
      </div>
    </div>
  );

  const MobileCard = ({ order, isLast }) => (
    // Mobile Card (Flex/Block)
    <div
      className={`lg:hidden p-4 mb-3 bg-white rounded-xl shadow-lg border ${
        !isLast ? "border-gray-200" : "border-transparent"
      }`}>
      <div className="flex justify-between items-center mb-2 pb-2 border-b">
        <span className="text-lg font-bold text-blue-700">
          Order ID: {order.id}
        </span>
        <StatusIndicator status={order.status} />
      </div>
      <div className="space-y-1 text-sm text-gray-700">
        <p>
          <strong>Customer:</strong> {order.customer}
        </p>
        <p>
          <strong>Device:</strong> {order.device}
        </p>
        <p>
          <strong>Issue:</strong> {order.issue}
        </p>
        <p>
          <strong>Date:</strong> {order.date}
        </p>
      </div>
      <div className="mt-4 flex justify-end">
        <button
          onClick={() => handleView(order.id)}
          className="px-4 py-2 bg-blue-600 text-white text-sm font-semibold rounded-xl shadow-md hover:bg-blue-700 transition-colors duration-200">
          view details
        </button>
      </div>
    </div>
  );

  // --- Main Render ---
  return (
    <div className="min-h-screen bg-gray-200 p-4 md:p-8 font-inter">
      <div className="max-w-7xl mx-auto">
        {/* Header Title */}
        <h1 className="text-3xl md:text-4xl font-extrabold text-blue-700 mb-6">
          My Orders
        </h1>

        {/* Filter and Controls Area */}
        <div className="bg-white p-4 md:p-6 rounded-2xl shadow-xl mb-6">
          <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
            {/* Dropdown for Mobile View */}
            <div className="lg:hidden w-full">
              <label
                htmlFor="order-status-select"
                className="block text-sm font-medium text-gray-700 mb-1">
                Order Status
              </label>
              <select
                id="order-status-select"
                value={selectedDropdownStatus}
                onChange={(e) => setSelectedDropdownStatus(e.target.value)}
                className="block w-full rounded-xl border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 h-10 transition-all">
                <option value="All">All</option>
                {Object.keys(STATUS_CONFIG).map((status) => (
                  <option key={status} value={status}>
                    {status}
                  </option>
                ))}
              </select>
            </div>

            {/* Buttons for Desktop View */}
            <div className="hidden lg:block">
              <FilterButtons
                activeFilter={activeFilter}
                setActiveFilter={setActiveFilter}
              />
            </div>
          </div>
        </div>

        {/* Orders Table/List */}
        <div className="bg-white rounded-2xl shadow-xl overflow-hidden">
          <div className="p-4 lg:p-0">
            {/* Table for Large Screens */}
            <TableHeader />

            <div className="divide-y divide-gray-100">
              {filteredOrders.length > 0 ? (
                filteredOrders.map((order, index) => (
                  <React.Fragment key={order.id}>
                    <TableRow
                      order={order}
                      isLast={index === filteredOrders.length - 1}
                    />
                    <MobileCard
                      order={order}
                      isLast={index === filteredOrders.length - 1}
                    />
                  </React.Fragment>
                ))
              ) : (
                <div className="p-8 text-center text-gray-500">
                  No orders found with status:{" "}
                  <span className="font-semibold text-gray-700">
                    {currentFilter}
                  </span>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MyOrder;
