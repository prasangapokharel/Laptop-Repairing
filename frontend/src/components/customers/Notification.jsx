import { CheckCircle, DollarSign, LayoutDashboard } from "lucide-react";
import React from "react";
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
export default function Notification() {
  return (
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
}
