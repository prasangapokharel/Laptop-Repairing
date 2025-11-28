import React from "react";
const recentOrdersData = [
  { id: "12345", date: "2025/01/22", status: "Active", amount: "Rs.0000" },
  { id: "56789", date: "2024/09/29", status: "Active", amount: "Rs.0000" },
  { id: "01234", date: "2024/06/31", status: "Active", amount: "Rs.0000" },
];
export default function RecentOrder() {
  return (
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
}
