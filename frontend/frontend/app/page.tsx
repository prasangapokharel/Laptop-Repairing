import Link from "next/link";

export default function Home() {
  return (
    <div className="font-sans bg-gray-50 min-h-screen">
      {/* Hero Section */}
      <section className="w-full flex flex-col items-center text-center py-20 px-6 bg-gradient-to-br from-blue-600 to-blue-400 text-white">
        <h1 className="text-4xl sm:text-5xl font-bold mb-4">
          Laptop Repairing Center
        </h1>
        <p className="text-lg sm:text-xl max-w-2xl">
          Fast, reliable and affordable laptop repair services.  
          We treat your laptop like it’s ours.
        </p>

        <div className="mt-8">
          <Link
            href="/customer/homepage"
            className="bg-white text-blue-600 px-6 py-3 rounded-lg font-medium shadow-md hover:scale-105 transition hover:shadow-lg hover:bg-blue-600 hover:text-white"
          >
            Go to Home Page
          </Link>
        </div>
      </section>

      {/* Services Section */}
      <section id="services" className="py-16 px-6">
        <h2 className="text-3xl font-bold text-center mb-10">Our Services</h2>

        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-8 max-w-6xl mx-auto">
          {[
            "Screen Replacement",
            "Battery Replacement",
            "Keyboard Repair",
            "Software Installation",
            "Virus Removal",
            "Hardware Upgrade",
          ].map((service) => (
            <div
              key={service}
              className="p-6 bg-white shadow rounded-xl hover:shadow-lg hover:-translate-y-1 transition"
            >
              <h3 className="text-lg font-semibold mb-2">{service}</h3>
              <p className="text-gray-600 text-sm">
                Professional and fast service with complete quality assurance.
              </p>
            </div>
          ))}
        </div>
      </section>

      {/* Why Choose Us */}
      <section className="py-16 bg-blue-50 px-6">
        <h2 className="text-3xl font-bold text-center mb-10">Why Choose Us?</h2>

        <div className="grid sm:grid-cols-3 gap-8 max-w-5xl mx-auto">
          <div className="p-6 bg-white shadow rounded-xl text-center">
            <h3 className="text-xl font-semibold">Experienced Technicians</h3>
            <p className="text-gray-600 mt-2 text-sm">
              Skilled experts who diagnose and fix issues efficiently.
            </p>
          </div>

          <div className="p-6 bg-white shadow rounded-xl text-center">
            <h3 className="text-xl font-semibold">Affordable Pricing</h3>
            <p className="text-gray-600 mt-2 text-sm">
              Transparent and budget friendly service charges.
            </p>
          </div>

          <div className="p-6 bg-white shadow rounded-xl text-center">
            <h3 className="text-xl font-semibold">Fast Service</h3>
            <p className="text-gray-600 mt-2 text-sm">
              Same-day service options available for common issues.
            </p>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-8 text-center text-gray-600 text-sm">
        © {new Date().getFullYear()} Laptop Repairing Center  
        <br />
        All Rights Reserved.
      </footer>
    </div>
  );
}
