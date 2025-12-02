import React from "react";
import { User } from "lucide-react";
import StatCard from "./StatCard";
import RecentOrder from "./RecentOrder";
import QuickAction from "./QuickAction";
import Notification from "./Notification";

export default function HomePage() {
  return (
    <main className="flex-1 p-4 sm:p-6 md:p-8">
      {/* Welcome Header and User Profile */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center pb-6 border-b border-gray-300 mb-6">
        <h1 className="text-3xl font-bold text-blue-800 mb-4 md:mb-0">
          Welcome Ram Bahadur
        </h1>

        <div className="bg-white p-4 rounded-xl shadow-md flex items-center space-x-4 border border-gray-200">
          <div className="shrink-0">
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
            <p className="text-xs text-gray-500">E-mail: rambdr24@gmail.com</p>
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
      <RecentOrder />

      {/* Quick Actions */}
      <QuickAction />

      {/* Notifications */}
      <Notification />
    </main>
  );
}
