import React from "react";
import User from "../assets/user.jpg";
import { IoIosArrowDown } from "react-icons/io";
import { FaEye, FaPlus } from "react-icons/fa";
import Image from "next/image";

export default function page() {
  return (
    <div
      className="min-h-screen w-full flex justify-center items-start "
      style={{
        background:
          "linear-gradient(100deg, rgba(30, 60, 114, 0.7) 10%, rgba(42, 82, 152, 0.7) 20%)",
      }}>
      <div className="w-full max-w-5xl min-h-screen bg-[#D1D5DB] rounded-lg  mt-10">
        <div className="w-full h-[104px] bg-[#1E40AF] rounded-t-lg py-5 px-4">
          <h1 className="font-bold text-white sm:text-4xl text-3xl">
            Customer Dashboard
          </h1>
        </div>
        {/* profile section */}
        <div className="flex mt-4 md:flex-row flex-col gap-6 rounded-lg">
          <div className="px-4 py-6">
            <h1 className="text-2xl font-bold">Welcome Pankaj Chaudhary</h1>
          </div>
          <div className="flex gap-4 ml-auto mr-5">
            <div className="w-[106px] h-[109px] border border-black rounded-full flex items-center justify-center">
              {/* <img className="w-full h-full rounded-full" src="../../assets/user.jpg" alt="" /> */}
              {/* <Image src="/public/assets/user.jpg" alt="" width={100} height={100} /> */}
              
            </div>
            <div className="text-2xl  ">
              <h1 className="font-bold">Pankaj Chaudhary</h1>
              <p>ID:0987654</p>
              <p>E-mail:pankaj@gmail.com</p>
            </div>
          </div>
        </div>
        {/* orders section */}
        <div className="flex gap-4 m-5 md:flex-row md:gap-10 flex-col">
          <div className="w-[550px] h-[250px] flex flex-col gap-7 bg-[#3d75ee] rounded-2xl px-5 py-5">
            <div className="w-[85px] h-[70px] bg-[#2563EB] flex items-center justify-center rounded-lg shadow-2xl">
              <IoIosArrowDown className="h-[60px] w-[60px] text-white" />
            </div>
            <div className="flex gap-10 font-bold text-white">
              <h1> Active order</h1>
              <p className="ml-auto mr-5">5</p>
            </div>
          </div>
          <div className="w-[550px] h-[250px] flex flex-col gap-7 bg-[#4ee2b1] rounded-2xl px-5 py-5">
            <div className="w-[85px] h-[70px] bg-[#10B981] flex items-center justify-center rounded-lg shadow-2xl">
              <IoIosArrowDown className="h-[60px] w-[60px] text-white" />
            </div>
            <div className="flex gap-10 font-bold text-white">
              <h1> Pending order</h1>
              <p className="ml-auto mr-5">5</p>
            </div>
          </div>
        </div>
        {/* more details section */}
        <div className="flex m-5 gap-5">
          <div className="w-[650px] h-[606px] border-blue-500 border-2 rounded-2xl">
            <div className="p-3 ">
              <h1 className="text-4xl font-bold">Recent Order</h1>
              <div className="h-[520px] overflow-y-auto mt-3">
                <table>
                  <thead>
                    <tr className="text-2xl bg-blue-300 ">
                      <th className="px-4 py-2 text-left">Order ID</th>
                      <th className="px-4 py-2 text-left">Date</th>
                      <th className="px-4 py-2 text-left">Status</th>
                      <th className="px-4 py-2 text-left">Amount</th>
                    </tr>
                  </thead>
                  <tbody className="text-2xl">
                    <tr className="border-b border-blue-300">
                      <td className="px-4 py-2 text-left">123</td>
                      <td className="px-4 py-2 text-left">2025/11/16</td>
                      <td className="px-4 py-2 text-left">pending</td>
                      <td className="px-4 py-2 text-left">5000</td>
                    </tr>

                    <tr className="border-b border-blue-300">
                      <td className="px-4 py-2 text-left">123</td>
                      <td className="px-4 py-2 text-left">2025/11/16</td>
                      <td className="px-4 py-2 text-left">pending</td>
                      <td className="px-4 py-2 text-left">5000</td>
                    </tr>

                    <tr className="border-b border-blue-300">
                      <td className="px-4 py-2 text-left">123</td>
                      <td className="px-4 py-2 text-left">2025/11/16</td>
                      <td className="px-4 py-2 text-left">pending</td>
                      <td className="px-4 py-2 text-left">5000</td>
                    </tr>

                    <tr className="border-b border-blue-300">
                      <td className="px-4 py-2 text-left">123</td>
                      <td className="px-4 py-2 text-left">2025/11/16</td>
                      <td className="px-4 py-2 text-left">pending</td>
                      <td className="px-4 py-2 text-left">5000</td>
                    </tr>

                    <tr className="border-b border-blue-300">
                      <td className="px-4 py-2 text-left">123</td>
                      <td className="px-4 py-2 text-left">2025/11/16</td>
                      <td className="px-4 py-2 text-left">pending</td>
                      <td className="px-4 py-2 text-left">5000</td>
                    </tr>

                    <tr className="border-b border-blue-300">
                      <td className="px-4 py-2 text-left">123</td>
                      <td className="px-4 py-2 text-left">2025/11/16</td>
                      <td className="px-4 py-2 text-left">pending</td>
                      <td className="px-4 py-2 text-left">5000</td>
                    </tr>

                    <tr className="border-b border-blue-300">
                      <td className="px-4 py-2 text-left">123</td>
                      <td className="px-4 py-2 text-left">2025/11/16</td>
                      <td className="px-4 py-2 text-left">pending</td>
                      <td className="px-4 py-2 text-left">5000</td>
                    </tr>

                    <tr className="border-b border-blue-300">
                      <td className="px-4 py-2 text-left">123</td>
                      <td className="px-4 py-2 text-left">2025/11/16</td>
                      <td className="px-4 py-2 text-left">pending</td>
                      <td className="px-4 py-2 text-left">5000</td>
                    </tr>

                    <tr className="border-b border-blue-300">
                      <td className="px-4 py-2 text-left">123</td>
                      <td className="px-4 py-2 text-left">2025/11/16</td>
                      <td className="px-4 py-2 text-left">pending</td>
                      <td className="px-4 py-2 text-left">5000</td>
                    </tr>

                    <tr className="border-b border-blue-300">
                      <td className="px-4 py-2 text-left">123</td>
                      <td className="px-4 py-2 text-left">2025/11/16</td>
                      <td className="px-4 py-2 text-left">pending</td>
                      <td className="px-4 py-2 text-left">5000</td>
                    </tr>
                    <tr className="border-b border-blue-300">
                      <td className="px-4 py-2 text-left">123</td>
                      <td className="px-4 py-2 text-left">2025/11/16</td>
                      <td className="px-4 py-2 text-left">pending</td>
                      <td className="px-4 py-2 text-left">5000</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
          <div className="w-[443px] h-[606px] border-blue-500 border-2 rounded-2xl flex flex-col gap-5 p-3">
            <h1 className="text-4xl font-bold ">Quick Actions</h1>
            <div className="flex gap-2 bg-blue-500 w-[395px] h-[220px] rounded-4xl items-center justify-center p-5 mt-5 shadow" >
              <div>
                <FaEye className="w-[88px] h-[63px] text-white"/>
              </div>
              <div>
                <h1 className="text-white text-3xl font-bold">View Devices</h1>
              </div>
            </div>

             <div className="flex gap-2 bg-blue-500 w-[395px] h-[220px] rounded-4xl items-center justify-center p-5 shadow" >
              <div>
                <FaPlus className="w-[88px] h-[63px] text-white"/>
              </div>
              <div>
                <h1 className="text-white text-3xl font-bold">Create Order</h1>
              </div>
            </div>
          </div>
        </div>
        {/* notfication section */}
        {/* <div className="w-[1103px] h-[472px] rounded-lg border-blue-500 border-2">
          <div className="p-5">
            <h1>Notifications</h1>
          </div>
        </div> */}
      </div>
    </div>
  );
}
