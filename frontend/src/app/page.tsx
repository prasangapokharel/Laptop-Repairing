import Link from 'next/link'

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <div className="z-10 max-w-5xl w-full items-center justify-between font-mono text-sm">
        <h1 className="text-4xl font-bold mb-8">Welcome to Dashboard</h1>
        <div className="flex gap-4">
          <Link href="/dashboard" className="px-4 py-2 bg-blue-500 text-white rounded">
            Dashboard
          </Link>
          <Link href="/user/add" className="px-4 py-2 bg-green-500 text-white rounded">
            Add User
          </Link>
        </div>
      </div>
    </main>
  )
}
