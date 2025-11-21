import React, { useState } from "react";
import {
  Home,
  Laptop,
  Package,
  ClipboardList,
  DollarSign,
  Menu,
  X,
  ChevronDown,
  CheckCircle,
  Bell,
  PlusCircle,
  LayoutDashboard,
  User,
} from "lucide-react";

// --- Configuration Data ---

const navItems = [
  { icon: Home, label: "Home" },
  { icon: Laptop, label: "My Device" },
  { icon: Package, label: "My Order" },
  { icon: ClipboardList, label: "Order Details" },
  { icon: DollarSign, label: "Payment" },
];

const recentOrdersData = [
  { id: "12345", date: "2025/01/22", status: "Active", amount: "Rs.0000" },
  { id: "56789", date: "2024/09/29", status: "Active", amount: "Rs.0000" },
  { id: "01234", date: "2024/06/31", status: "Active", amount: "Rs.0000" },
];

const notificationsData = [
  {
    icon: CheckCircle,
    text: "Your order has been created",
    date: "2025/01/22",
    color: "text-green-500",
  },
  {
    icon: DollarSign,
    text: "Payment reminder for order 12345",
    date: "2024/09/29",
    color: "text-blue-500",
  },
  {
    icon: LayoutDashboard,
    text: "Your profile has been updated",
    date: "2024/06/31",
    color: "text-yellow-500",
  },
];

// --- Sub-Components ---

/**
 * Renders a single navigation link in the sidebar.
 * @param {object} props - Component props.
 * @param {object} props.icon - Lucide React icon component.
 * @param {string} props.label - The link text.
 * @param {boolean} props.isActive - Whether the link is currently active.
 */
const NavItem = ({ icon: Icon, label, isActive }) => (
  <a
    href="#"
    className={`flex items-center p-3 text-sm font-medium transition-colors duration-200 ${
      isActive
        ? "bg-blue-600 text-white rounded-r-full shadow-lg"
        : "text-blue-200 hover:bg-blue-700 hover:text-white rounded-r-full"
    }`}>
    <Icon className="w-5 h-5 mr-4" />
    <span>{label}</span>
  </a>
);

/**
 * Renders the main fixed sidebar navigation.
 * @param {object} props - Component props.
 * @param {boolean} props.isOpen - Whether the mobile menu is open.
 * @param {function} props.onClose - Function to close the mobile menu.
 */
const Sidebar = ({ isOpen, onClose }) => (
  <>
    {/* Overlay for mobile view */}
    <div
      className={`fixed inset-0 z-40 bg-black bg-opacity-50 lg:hidden transition-opacity ${
        isOpen ? "opacity-100 visible" : "opacity-0 invisible"
      }`}
      onClick={onClose}
    />

    {/* Sidebar Content */}
    <div
      className={`fixed inset-y-0 left-0 z-50 w-64 bg-blue-800 transform lg:translate-x-0 transition-transform duration-300 ease-in-out shadow-2xl ${
        isOpen ? "translate-x-0" : "-translate-x-full"
      }`}>
      <div className="flex items-center justify-between p-5 h-16 bg-blue-900 border-b border-blue-700">
        <h1 className="text-xl font-bold text-white flex items-center">
          <LayoutDashboard className="w-6 h-6 mr-2" />
          Dashboard
        </h1>
        <button
          onClick={onClose}
          className="text-blue-200 lg:hidden hover:text-white transition-colors">
          <X className="w-6 h-6" />
        </button>
      </div>
      <nav className="flex flex-col space-y-2 p-4 pt-8">
        {navItems.map((item, index) => (
          <NavItem
            key={item.label}
            icon={item.icon}
            label={item.label}
            // 'Home' is set as the active item based on the design image
            isActive={item.label === "Home"}
          />
        ))}
      </nav>
    </div>
  </>
);

/**
 * Renders a statistic card (Active or Pending Orders).
 * @param {object} props - Component props.
 * @param {string} props.title - The card title.
 * @param {number} props.count - The order count.
 * @param {string} props.bgColor - Tailwind background color class.
 * @param {string} props.arrowColor - Tailwind text color for the arrow.
 */
const StatCard = ({ title, count, bgColor, arrowColor }) => (
  <div
    className={`flex flex-col p-6 rounded-xl shadow-lg ${bgColor} text-white transition-transform hover:scale-[1.01] duration-300`}>
    <div className="flex justify-between items-center mb-2">
      <h3 className="text-lg font-semibold">{title}</h3>
      <ChevronDown className={`w-6 h-6 ${arrowColor}`} />
    </div>
    <span className="text-4xl font-extrabold">{count}</span>
    <span className="text-sm opacity-80">Total {title.toLowerCase()}</span>
  </div>
);

/**
 * Renders the Recent Orders table component.
 */
const RecentOrders = () => (
  <div className="bg-white p-6 rounded-xl shadow-lg mt-6">
    <h2 className="text-2xl font-bold text-gray-800 mb-4">Recent Orders</h2>
    <div className="overflow-x-auto">
      <table className="min-w-full divide-y divide-gray-200">
        <thead className="bg-gray-50">
          <tr>
            {["Order ID", "Date", "Status", "Amount"].map((header) => (
              <th
                key={header}
                scope="col"
                className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                {header}
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-200">
          {recentOrdersData.map((order, index) => (
            <tr key={order.id} className="hover:bg-blue-50 transition-colors">
              <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                {order.id}
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {order.date}
              </td>
              <td className="px-6 py-4 whitespace-nowrap">
                <span className="px-3 py-1 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-500 text-white">
                  {order.status}
                </span>
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {order.amount}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
    <div className="mt-4 flex justify-end">
      <button className="text-blue-600 hover:text-blue-800 font-medium py-2 px-4 rounded-lg transition-colors border border-blue-600 hover:bg-blue-50">
        View All
      </button>
    </div>
  </div>
);

/**
 * Renders the Quick Actions buttons.
 */
const QuickActions = () => (
  <div className="mt-8">
    <h2 className="text-2xl font-bold text-gray-800 mb-4">Quick Actions</h2>
    <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
      {/* View Devices Card */}
      <button className="flex items-center justify-center p-6 text-xl font-semibold text-white bg-blue-700 rounded-xl shadow-lg transition-all hover:bg-blue-800 hover:shadow-xl transform hover:-translate-y-0.5">
        <Laptop className="w-6 h-6 mr-3" />
        View Devices
      </button>

      {/* Create Order Card */}
      <button className="flex items-center justify-center p-6 text-xl font-semibold text-white bg-blue-700 rounded-xl shadow-lg transition-all hover:bg-blue-800 hover:shadow-xl transform hover:-translate-y-0.5">
        <PlusCircle className="w-6 h-6 mr-3" />
        Create Order
      </button>
    </div>
  </div>
);

/**
 * Renders the Notifications list.
 */
const Notifications = () => (
  <div className="bg-white p-6 rounded-xl shadow-lg mt-8">
    <h2 className="text-2xl font-bold text-gray-800 mb-4">Notifications</h2>
    <div className="space-y-4">
      {notificationsData.map((notification, index) => (
        <div
          key={index}
          className="flex justify-between items-center border-b pb-3 last:border-b-0 last:pb-0">
          <div className="flex items-center">
            <notification.icon
              className={`w-5 h-5 mr-3 ${notification.color}`}
            />
            <span className="text-gray-700">{notification.text}</span>
          </div>
          <span className="text-sm text-gray-400 font-light">
            {notification.date}
          </span>
        </div>
      ))}
    </div>
  </div>
);

// --- Main App Component ---

const CustomerDashboard = () => {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  const toggleSidebar = () => {
    setIsSidebarOpen(!isSidebarOpen);
  };

  const closeSidebar = () => {
    setIsSidebarOpen(false);
  };

  return (
    <div className="min-h-screen bg-gray-100 flex font-inter">
      {/* 1. Sidebar */}
      <Sidebar isOpen={isSidebarOpen} onClose={closeSidebar} />

      {/* 2. Main Content Area */}
      <div className="flex-1 lg:ml-64 flex flex-col">
        {/* Header/Top Bar (Visible on Mobile to access menu) */}
        <header className="sticky top-0 z-30 bg-blue-900 lg:hidden flex items-center justify-between p-4 h-16 shadow-md">
          <h1 className="text-xl font-bold text-white">Dashboard</h1>
          <button
            onClick={toggleSidebar}
            className="text-white hover:text-blue-200">
            <Menu className="w-6 h-6" />
          </button>
        </header>

        {/* Inner Content */}
        <main className="flex-1 p-4 sm:p-6 md:p-8">
          {/* Welcome Header and User Profile */}
          <div className="flex flex-col md:flex-row justify-between items-start md:items-center pb-6 border-b border-gray-300 mb-6">
            <h1 className="text-3xl font-bold text-blue-800 mb-4 md:mb-0">
              Welcome Ram Bahadur
            </h1>

            <div className="bg-white p-4 rounded-xl shadow-md flex items-center space-x-4 border border-gray-200">
              <div className="flex-shrink-0">
                <img
                  className="h-12 w-12 rounded-full object-cover border-2 border-blue-500"
                  src="https://placehold.co/100x100/3B82F6/ffffff?text=RB"
                  alt="User Avatar"
                  onError={(e) => {
                    e.target.onerror = null;
                    e.target.src =
                      "https://placehold.co/100x100/3B82F6/ffffff?text=User";
                  }}
                />
              </div>
              <div>
                <p className="text-sm font-semibold text-gray-900 flex items-center">
                  Ram Bahadur <User className="w-4 h-4 ml-1 text-blue-500" />
                </p>
                <p className="text-xs text-gray-500">ID: CUST-001000</p>
                <p className="text-xs text-gray-500">
                  E-mail: rambdr24@gmail.com
                </p>
              </div>
            </div>
          </div>

          {/* Stat Cards (Active/Pending Orders) */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-2 gap-6">
            <StatCard
              title="Active Orders"
              count={5}
              bgColor="bg-blue-600"
              arrowColor="text-blue-200"
            />
            <StatCard
              title="Pending Orders"
              count={2}
              bgColor="bg-green-600"
              arrowColor="text-green-200"
            />
          </div>

          {/* Recent Orders Table */}
          <RecentOrders />

          {/* Quick Actions */}
          <QuickActions />

          {/* Notifications */}
          <Notifications />
        </main>
      </div>
    </div>
  );
};

export default CustomerDashboard;
