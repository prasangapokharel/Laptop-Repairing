import React from "react";
import { ChevronDown } from "lucide-react";

export default function StatCard({ title, count, bgColor, arrowColor }) {
  return (
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
}
