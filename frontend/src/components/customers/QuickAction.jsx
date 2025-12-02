import { Laptop, PlusCircle } from 'lucide-react'
import React from 'react'

export default function QuickAction() {
  return (
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
  )
}
