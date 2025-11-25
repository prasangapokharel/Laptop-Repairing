import React from "react";

// --- Sample Data ---

const ORDER_DATA = {
  orderId: "ORD-0001",
  status: "Pending",
  date: "24 Apr 2024, 10:30",
  customerName: "Ram Bahadur",
  customerEmail: "ram003.bdr@gmail.com",

  device: {
    type: "Laptop",
    brand: "Dell",
    model: "Inspiron 5570",
    serial: "SN 9B-PB4-LP-552",
    problemDesc: "Laptop not booting up",
    additionalNotes: "Unable to find the issue",
  },

  payment: {
    status: "Paid",
    method: "Online",
    transactionId: "TX11245",
    amount: 3300,
    remainingBalance: 0,
  },

  condition: {
    scratches: "Yes",
    physicalDamage: "No",
    accessories: "Charger, Bag, Mouse",
  },

  cost: {
    items: [
      { name: "Service Charge", price: 1000 },
      { name: "Replacement Part (Keyboard)", price: 2000 },
      { name: "Diagnostic Fee", price: 500 },
      { name: "Discount", price: -200 },
    ],
    total: 3300,
  },

  statusHistory: [
    {
      label: "Order Received",
      date: "24 Apr 2024, 10:30 AM",
      type: "completed",
    },
    { label: "Diagnosis In Progress", date: "24 Apr 2024", type: "completed" },
    { label: "Repairing", date: "2 Apr 2024", type: "current" },
    { label: "Quality Check", date: "3 Apr 2024", type: "pending" },
    { label: "Ready for Pickup", date: "3 Apr 2024", type: "pending" },
  ],
};

// --- Utility Functions ---

const getStatusClasses = (status) => {
  switch (status) {
    case "Pending":
      return "bg-orange-500 text-white shadow-md shadow-orange-500/30";
    case "Paid":
      return "bg-green-500 text-white shadow-md shadow-green-500/30";
    case "Repairing":
    case "Completed":
      return "bg-blue-600 text-white shadow-md shadow-blue-600/30";
    default:
      return "bg-gray-400 text-white shadow-md shadow-gray-400/30";
  }
};

const InfoRow = ({
  label,
  value,
  valueClassName = "font-semibold text-gray-800",
}) => (
  <div className="flex justify-between md:justify-start md:gap-x-8 mb-2">
    <span className="text-gray-600 w-2/5 md:w-auto md:min-w-[180px] font-medium text-sm sm:text-base">
      {label}:
    </span>

    <span
      className={`text-right md:text-left w-3/5 md:w-auto ${valueClassName} break-words text-sm sm:text-base`}>
      {value}
    </span>
  </div>
);

const Card = ({
  title,
  children,
  bgColor = "bg-white",
  titleColor = "text-gray-900",
}) => (
  <div
    className={`rounded-xl shadow-lg p-5 md:p-6 ${bgColor} mb-6 transition-all duration-300 hover:shadow-xl hover:scale-[1.01]`}>
    <h2
      className={`text-lg sm:text-xl font-bold ${titleColor} mb-4 border-b border-gray-300/50 pb-2`}>
      {title}
    </h2>
    {children}
  </div>
);

// --- Status History Timeline ---
const StatusHistory = ({ history }) => {
  const getTimelineStyle = (type) => {
    switch (type) {
      case "completed":
        return {
          icon: "text-white bg-blue-600 ring-2 ring-blue-300",
          line: "bg-blue-300",
          text: "text-blue-700",
        };
      case "current":
        return {
          icon: "text-blue-600 bg-white border-2 border-blue-600 ring-4 ring-blue-100",
          line: "bg-gray-300",
          text: "text-blue-800 font-bold",
        };
      case "pending":
        return {
          icon: "text-gray-400 bg-white border-2 border-gray-400",
          line: "bg-gray-300",
          text: "text-gray-600",
        };
      default:
        return {
          icon: "bg-gray-400",
          line: "bg-gray-300",
          text: "text-gray-600",
        };
    }
  };

  return (
    <Card
      title="Status History"
      bgColor="bg-gray-200/50"
      titleColor="text-gray-700">
      <div className="relative pl-6 sm:pl-8">
        {history.map((item, index) => {
          const style = getTimelineStyle(item.type);
          const isLast = index === history.length - 1;

          return (
            <div key={index} className="flex mb-8 last:mb-0 items-start">
              {!isLast && (
                <div
                  className={`absolute left-[11.5px] sm:left-[13.5px] top-4 bottom-[-10px] w-0.5 ${style.line}`}></div>
              )}

              <div
                className={`relative z-10 w-5 h-5 sm:w-6 sm:h-6 rounded-full flex items-center justify-center text-xs font-bold mr-3 ${style.icon}`}>
                {item.type === "completed" && (
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    className="h-3 w-3"
                    viewBox="0 0 20 20"
                    fill="currentColor">
                    <path
                      fillRule="evenodd"
                      d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                      clipRule="evenodd"
                    />
                  </svg>
                )}
                {item.type === "current" && (
                  <div className="w-2 h-2 rounded-full bg-blue-600"></div>
                )}
              </div>

              <div className="flex-1 min-w-0 pt-0.5">
                <p className={`text-sm sm:text-base ${style.text}`}>
                  {item.label}
                </p>
                <p className="text-xs sm:text-sm text-gray-500">{item.date}</p>
              </div>
            </div>
          );
        })}
      </div>
    </Card>
  );
};

// --- Section Components ---
const DeviceInformationSection = ({ data }) => (
  <Card
    title="Device Information"
    bgColor="bg-blue-100/50"
    titleColor="text-blue-700">
    <div className="space-y-2">
      <InfoRow label="Device Type" value={data.device.type} />
      <InfoRow label="Brand" value={data.device.brand} />
      <InfoRow label="Model" value={data.device.model} />
      <InfoRow label="Serial Number" value={data.device.serial} />
      <InfoRow label="Problem Desc." value={data.device.problemDesc} />
      <InfoRow label="Additional Notes" value={data.device.additionalNotes} />
    </div>
  </Card>
);

const PaymentInformationSection = ({ data }) => (
  <Card
    title="Payment Information"
    bgColor="bg-gray-100/50"
    titleColor="text-gray-700">
    <div className="space-y-2">
      <InfoRow
        label="Payment Status"
        value={data.payment.status}
        valueClassName={`${getStatusClasses(
          data.payment.status
        )} px-3 py-1 text-xs font-bold rounded-full`}
      />
      <InfoRow label="Payment Method" value={data.payment.method} />
      <InfoRow label="Transaction ID" value={data.payment.transactionId} />
      <InfoRow
        label="Amount Paid"
        value={`Rs. ${data.payment.amount.toLocaleString()}`}
      />
      <InfoRow
        label="Remaining Balance"
        value={`Rs. ${data.payment.remainingBalance.toLocaleString()}`}
      />
    </div>
  </Card>
);

const DeviceConditionSection = ({ data }) => (
  <Card
    title="Device Condition on Arrival"
    bgColor="bg-blue-100/50"
    titleColor="text-blue-700">
    <div className="space-y-2">
      <InfoRow label="Scratches" value={data.condition.scratches} />
      <InfoRow label="Physical Damage" value={data.condition.physicalDamage} />
      <InfoRow
        label="Accessories Included"
        value={data.condition.accessories}
      />
    </div>
  </Card>
);

const CostBreakdownSection = ({ data }) => (
  <Card
    title="Cost Breakdown"
    bgColor="bg-gray-100/50"
    titleColor="text-gray-700">
    <div className="space-y-2 text-sm sm:text-base">
      {data.cost.items.map((item) => (
        <div
          key={item.name}
          className="flex justify-between pb-2 border-b border-gray-300/50 last:border-b-0">
          <span className="text-gray-600">{item.name}</span>
          <span
            className={`font-medium ${
              item.price < 0 ? "text-red-600" : "text-gray-800"
            }`}>
            {item.price < 0
              ? `- Rs. ${Math.abs(item.price).toLocaleString()}`
              : `Rs. ${item.price.toLocaleString()}`}
          </span>
        </div>
      ))}

      <div className="flex justify-between pt-3 font-extrabold text-xl border-t-2 border-blue-200">
        <span>Total</span>
        <span className="text-blue-700">
          Rs. {data.cost.total.toLocaleString()}
        </span>
      </div>
    </div>
  </Card>
);

// --- Main Component ---
const OrderDetails = () => {
  const data = ORDER_DATA;
  const statusClasses = getStatusClasses(data.status);

  return (
    <div className="min-h-screen bg-gray-50 p-4 md:p-8 font-inter antialiased">
      <div className="max-w-5xl mx-auto">
        {/* Header */}
        <header className="flex flex-col md:flex-row justify-between items-start md:items-center mb-8 border-b-2 border-gray-300 pb-4 gap-4">
          <div>
            <h1 className="text-3xl sm:text-4xl font-extrabold text-blue-700">
              Order Details
            </h1>
            <p className="text-lg sm:text-xl text-gray-500 font-medium mt-1">
              {data.orderId}
            </p>
          </div>

          <div className="text-right p-4 rounded-xl shadow-lg bg-white border border-gray-200 min-w-[200px] transition-all duration-300 hover:scale-[1.01]">
            <span
              className={`inline-block px-4 py-1 text-xs font-bold rounded-lg mb-2 ${statusClasses}`}>
              {data.status}
            </span>
            <p className="text-sm text-gray-600">{data.date}</p>
            <p className="text-md font-semibold text-gray-800 mt-1">
              {data.customerName}
            </p>
            <p className="text-xs text-blue-500 break-all">
              {data.customerEmail}
            </p>
          </div>
        </header>

        {/* Grid */}
        <main className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 space-y-6">
            <DeviceInformationSection data={data} />
            <DeviceConditionSection data={data} />
          </div>

          <div className="lg:col-span-1 space-y-6">
            <PaymentInformationSection data={data} />
            <CostBreakdownSection data={data} />
          </div>

          <div className="lg:col-span-3">
            <StatusHistory history={data.statusHistory} />
          </div>
        </main>
      </div>
    </div>
  );
};

export default OrderDetails;
