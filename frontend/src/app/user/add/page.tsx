'use client'

import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { apiClient } from '@/lib/api-client'
import { useRouter } from 'next/navigation'

const userSchema = z.object({
  username: z.string().min(3, 'Username must be at least 3 characters'),
  email: z.string().email('Invalid email address'),
  first_name: z.string().optional(),
  last_name: z.string().optional(),
})

type UserFormData = z.infer<typeof userSchema>

export default function AddUserPage() {
  const router = useRouter()
  const queryClient = useQueryClient()
  
  const { register, handleSubmit, formState: { errors } } = useForm<UserFormData>({
    resolver: zodResolver(userSchema),
  })

  const mutation = useMutation({
    mutationFn: async (data: UserFormData) => {
      const response = await apiClient.post('/users/', data)
      return response.data
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['users'] })
      router.push('/dashboard')
    },
  })

  const onSubmit = (data: UserFormData) => {
    mutation.mutate(data)
  }

  return (
    <div className="container mx-auto p-8 max-w-2xl">
      <h1 className="text-3xl font-bold mb-6">Add User</h1>
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        <div>
          <label className="block mb-2">Username</label>
          <input
            {...register('username')}
            className="w-full p-2 border rounded"
            type="text"
          />
          {errors.username && (
            <p className="text-red-500 text-sm mt-1">{errors.username.message}</p>
          )}
        </div>

        <div>
          <label className="block mb-2">Email</label>
          <input
            {...register('email')}
            className="w-full p-2 border rounded"
            type="email"
          />
          {errors.email && (
            <p className="text-red-500 text-sm mt-1">{errors.email.message}</p>
          )}
        </div>

        <div>
          <label className="block mb-2">First Name</label>
          <input
            {...register('first_name')}
            className="w-full p-2 border rounded"
            type="text"
          />
        </div>

        <div>
          <label className="block mb-2">Last Name</label>
          <input
            {...register('last_name')}
            className="w-full p-2 border rounded"
            type="text"
          />
        </div>

        <button
          type="submit"
          disabled={mutation.isPending}
          className="px-6 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 disabled:opacity-50"
        >
          {mutation.isPending ? 'Adding...' : 'Add User'}
        </button>

        {mutation.isError && (
          <p className="text-red-500">Error adding user. Please try again.</p>
        )}
      </form>
    </div>
  )
}
