import React, { useState } from "react";

const ContactSection = () => {
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    phone: "",
    projectDetails: "",
    interests: [],
  });

  const interestsList = [
    "Narrative Design",
    "AI Agents",
    "Game Mechanics",
    "Art Generation",
    "Voice / Dialogue",
    "Cinematic Design",
    "3D Environments",
    "World Building",
  ];

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleInterestToggle = (interest) => {
    setFormData((prev) => {
      const alreadySelected = prev.interests.includes(interest);
      return {
        ...prev,
        interests: alreadySelected
          ? prev.interests.filter((i) => i !== interest)
          : [...prev.interests, interest],
      };
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("Project Inquiry:", formData);
    alert("Thanks for your interest! We’ll get back to you soon.");
  };

  return (
    <section
      id="contact"
      className="relative min-h-screen bg-[#050505] text-gray-900 flex items-center justify-center  overflow-hidden px-25"
    >
      {/* Background Glow */}
      <div
        className="hero-glow absolute inset-0 z-0 scale-100 opacity-60 transition-all duration-700 
                   bg-[radial-gradient(circle_at_center,rgba(130,75,255,0.4)_0%,rgba(10,10,10,1)_80%)] 
                   blur-[180px]"
      ></div>

      {/* Contact Card */}
      <div className="relative z-10 bg-white rounded-3xl shadow-2xl p-8 sm:p-20 w-full max-w-full text-left">
        <h2 className="text-4xl font-Orbitron font-extrabold mb-8 text-gray-900 tracking-tight hidden">
          Let's Build Project <span className="text-purple-400">X</span> Together
        </h2>

        <form
          onSubmit={handleSubmit}
          className="space-y-10 text-gray-700 text-2xl text-left font-Manrope"
        >
          <p className="text-gray-900 text-2xl leading-relaxed">
            Hello! My name is{" "}
            <input
              type="text"
              name="name"
              placeholder="your full name"
              value={formData.name}
              onChange={handleChange}
              className="bg-transparent border-b-2 border-gray-300 focus:border-gray-600 outline-none px-2 mx-1 w-64 text-gray-900 placeholder-gray-400 text-2xl"
            />
            and I want to discuss a potential project. You can email me at{" "}
            <input
              type="email"
              name="email"
              placeholder="your@email.com"
              value={formData.email}
              onChange={handleChange}
              className="bg-transparent border-b-2 border-gray-300 focus:border-gray-600 outline-none px-2 mx-1 w-72 text-gray-900 placeholder-gray-400 text-2xl"
            />
            or reach me on{" "}
            <input
              type="text"
              name="phone"
              placeholder="your phone #"
              value={formData.phone}
              onChange={handleChange}
              className="bg-transparent border-b-2 border-gray-300 focus:border-gray-600 outline-none px-2 mx-1 w-56 text-gray-900 placeholder-gray-400 text-2xl"
            />
            .
          </p>

          <p className="text-gray-900 text-2xl">Here are some details about my project:</p>

          <textarea
            name="projectDetails"
            placeholder="My project is about..."
            value={formData.projectDetails}
            onChange={handleChange}
            rows={5}
            className="w-full bg-transparent border-b-2 border-gray-300 focus:border-gray-600 outline-none px-2 py-3 resize-none text-gray-900 placeholder-gray-400 text-xl"
          />

          <p className="mt-10 font-medium text-gray-900 text-2xl">
            I'm interested in <span className="text-gray-500">(select one or more)</span>:
          </p>

          {/* Interest Tags */}
          <div className="flex flex-wrap gap-5 mt-8">
            {interestsList.map((interest) => (
              <button
                type="button"
                key={interest}
                onClick={() => handleInterestToggle(interest)}
                className={`px-8 py-4 rounded-2xl border-2 text-lg font-medium transition-all duration-300 ${
                  formData.interests.includes(interest)
                    ? "bg-gray-900 text-white border-gray-900"
                    : "border-gray-300 text-gray-500 hover:text-gray-900 hover:border-gray-500"
                }`}
              >
                {interest}
              </button>
            ))}
          </div>

          <div className="text-center mt-14">
            <button
              type="submit"
              className="px-12 py-5 rounded-full border-2 border-purple-500 text-purple-500 font-semibold text-xl hover:bg-purple-500 hover:text-white transition-all duration-300 tracking-wide"
            >
              SEND REQUEST
            </button>
          </div>
        </form>
      </div>
    </section>
  );
};

export default ContactSection;
