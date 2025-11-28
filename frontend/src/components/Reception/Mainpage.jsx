import React from "react";
import {
  ShoppingCart,
  Wrench,
  CheckCircle,
  ClipboardList,
  UserPlus,
  Box,
  FilePlus,
} from "lucide-react";

// --- Mock Data ---
const MOCK_ORDERS = [
  { id: "001", customer: "Ram Bahadur", type: "Sales", device: "Dell XPS 13", status: "Pending" },
  { id: "002", customer: "Sita Kumari", type: "Repair", device: "MacBook Pro", status: "Pending" },
  { id: "003", customer: "Hari Maya", type: "Repair", device: "Lenovo", status: "Completed" },
  { id: "004", customer: "Rama Rai", type: "Repair", device: "Dell XPS 13", status: "Completed" },
  { id: "005", customer: "Maya Devi", type: "Repair", device: "MacBook Pro", status: "Completed" },
];

const PENDING_TASKS = [
  { id: 1, message: "3 laptops waiting for customer pickup" },
  { id: 2, message: "2 payments pending" },
  { id: 3, message: "1 low stock - Dell charger" },
  { id: 4, message: "2 laptops repair pending" },
];

// --- Sub Components ---
const StatCard = ({ icon: Icon, count, label, colorClass }) => (
  <div className="bg-gray-300 bg-opacity-50 rounded-xl p-6 shadow-sm relative overflow-hidden h-40">
    <div className={`absolute top-4 left-4 ${colorClass}`}>
      <Icon size={28} />
    </div>
    <div className="absolute bottom-4 left-4">
      <div className="text-3xl font-bold text-gray-800">{count}</div>
      <div className="text-sm font-semibold text-gray-700">{label}</div>
    </div>
  </div>
);

const QuickActionButton = ({ icon: Icon, label }) => (
  <button className="flex flex-col items-center justify-center bg-gray-300 bg-opacity-50 rounded-xl p-4 shadow-sm hover:shadow-md hover:bg-gray-200 transition-all h-32">
    <div className="mb-3 text-blue-600">
      <Icon size={24} />
    </div>
    <span className="text-sm font-bold text-gray-800 text-center">{label}</span>
  </button>
);

const StatusBadge = ({ status }) => {
  const isPending = status === "Pending";
  return (
    <span
      className={`px-3 py-1 rounded-full text-xs font-bold text-white ${
        isPending ? "bg-orange-400" : "bg-green-500"
      }`}
    >
      {status}
    </span>
  );
};

const TaskItem = ({ message }) => (
  <div className="bg-white rounded-full px-4 py-3 shadow-sm flex items-center gap-3 mb-2">
    <div className="bg-orange-400 rounded-full p-1 w-6 h-6 flex items-center justify-center text-white">
      <span className="text-xs font-bold">!</span>
    </div>
    <span className="text-sm font-medium text-gray-700">{message}</span>
  </div>
);

// --- Main Component ---
const Mainpage = () => {
  return (
    <main className="flex-1 p-6 lg:p-10 bg-white min-h-screen">

      {/* Header */}
      <div className="bg-[#2563EB] rounded-xl p-6 flex justify-between items-center text-white shadow-md mb-6">
        <h1 className="text-2xl font-bold">Reception Dashboard</h1>
        <button className="bg-white text-blue-600 px-4 py-2 rounded-lg font-semibold hover:bg-blue-50">
          Generate Report
        </button>
      </div>

      <div className="space-y-10">

        {/* Daily Statistics */}
        <section className="bg-gray-200 rounded-xl p-6 shadow-sm">
          <h2 className="text-lg font-bold mb-4 text-gray-900">Daily Statistics</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <StatCard icon={ShoppingCart} count={7} label="New Orders" colorClass="text-blue-600" />
            <StatCard icon={Wrench} count={3} label="Pending Orders" colorClass="text-blue-600" />
            <StatCard icon={CheckCircle} count={2} label="Completed Repairs" colorClass="text-green-500" />
          </div>
        </section>

        {/* Quick Actions */}
        <section className="bg-gray-200 rounded-xl p-6 shadow-sm">
          <h2 className="text-lg font-bold text-gray-900 mb-4">Quick Actions</h2>
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-4">
            <QuickActionButton icon={ClipboardList} label="Create Sales Order" />
            <QuickActionButton icon={UserPlus} label="Register Customer" />
            <QuickActionButton icon={Box} label="Check Inventory" />
            <QuickActionButton icon={Wrench} label="Create Repair Order" />
            <QuickActionButton icon={FilePlus} label="Generate Order" />
          </div>
        </section>

        {/* Recent Orders */}
        <section>
          <h2 className="text-xl font-bold text-gray-900 mb-4">Recent Orders</h2>
          <div className="bg-gray-200 rounded-xl p-4 shadow-sm border-2 border-blue-400 overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full min-w-[600px]">
                <thead>
                  <tr className="text-left text-black font-bold border-b border-gray-300">
                    <th className="pb-3 px-4">Order ID</th>
                    <th className="pb-3 px-4">Customer</th>
                    <th className="pb-3 px-4">Order Type</th>
                    <th className="pb-3 px-4">Device</th>
                    <th className="pb-3 px-4 text-center">Status</th>
                  </tr>
                </thead>

                <tbody className="text-sm">
                  {MOCK_ORDERS.map((order) => (
                    <tr key={order.id} className="border-b hover:bg-gray-300/20">
                      <td className="py-4 px-4 font-medium text-gray-800">{order.id}</td>
                      <td className="py-4 px-4 text-gray-700">{order.customer}</td>
                      <td className="py-4 px-4 text-gray-700">{order.type}</td>
                      <td className="py-4 px-4 text-gray-700">{order.device}</td>
                      <td className="py-4 px-4 text-center">
                        <StatusBadge status={order.status} />
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </section>

        {/* Pending Tasks */}
        <section>
          <h2 className="text-xl font-bold text-gray-900 mb-4">Pending Tasks</h2>
          <div className="bg-gray-200 rounded-xl p-6 shadow-sm">
            <div className="flex flex-col gap-2">
              {PENDING_TASKS.map((task) => (
                <TaskItem key={task.id} message={task.message} />
              ))}
            </div>
          </div>
        </section>
      </div>
    </main>
  );
};

export default Mainpage;
