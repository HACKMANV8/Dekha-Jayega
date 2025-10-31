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
      className="relative min-h-screen bg-[#050505] text-white flex items-center justify-center py-20 overflow-hidden"
    >
      {/* Background Glow */}
      <div
        className="absolute inset-0 z-0 opacity-60 blur-[180px]
        bg-[radial-gradient(circle_at_center,rgba(130,75,255,0.4)_0%,rgba(10,10,10,1)_80%)]"
      ></div>

      {/* Contact Card */}
      <div className="relative z-10 bg-black/40 backdrop-blur-xl border border-purple-700/40 rounded-3xl shadow-2xl p-10 sm:p-12 w-[90%] max-w-3xl text-center">
        <h2 className="text-4xl font-Orbitron font-extrabold mb-8 text-white tracking-tight">
          Let's Build Project <span className="text-purple-400">X</span> Together
        </h2>

        <form
          onSubmit={handleSubmit}
          className="space-y-6 text-gray-300 text-lg text-left"
        >
          <p>
            Hello! My name is{" "}
            <input
              type="text"
              name="name"
              placeholder="your full name"
              value={formData.name}
              onChange={handleChange}
              className="bg-transparent border-b border-purple-500/60 focus:border-purple-400 outline-none px-2 mx-2 w-48"
            />
            and I want to discuss a potential project. You can email me at{" "}
            <input
              type="email"
              name="email"
              placeholder="your@email.com"
              value={formData.email}
              onChange={handleChange}
              className="bg-transparent border-b border-purple-500/60 focus:border-purple-400 outline-none px-2 mx-2 w-56"
            />
            or reach me on{" "}
            <input
              type="text"
              name="phone"
              placeholder="your phone #"
              value={formData.phone}
              onChange={handleChange}
              className="bg-transparent border-b border-purple-500/60 focus:border-purple-400 outline-none px-2 mx-2 w-40"
            />
            .
          </p>

          <p>Here are some details about my project:</p>

          <textarea
            name="projectDetails"
            placeholder="My project is about..."
            value={formData.projectDetails}
            onChange={handleChange}
            rows={3}
            className="w-full bg-transparent border-b border-purple-500/60 focus:border-purple-400 outline-none px-2 py-3 resize-none"
          />

          <p className="mt-6 font-medium text-gray-300">
            I'm interested in <span className="text-purple-400">(select one or more)</span>:
          </p>

          {/* Interest Tags */}
          <div className="flex flex-wrap gap-3 mt-4">
            {interestsList.map((interest) => (
              <button
                type="button"
                key={interest}
                onClick={() => handleInterestToggle(interest)}
                className={`px-4 py-2 rounded-xl border text-sm font-medium transition-all duration-300 ${
                  formData.interests.includes(interest)
                    ? "bg-purple-600 text-white border-purple-400 shadow-lg shadow-purple-500/40"
                    : "border-purple-700/40 text-gray-400 hover:text-white hover:border-purple-400"
                }`}
              >
                {interest}
              </button>
            ))}
          </div>

          <div className="text-center mt-10">
            <button
              type="submit"
              className="px-8 py-3 rounded-full border border-purple-400 text-purple-300 font-semibold hover:bg-purple-500 hover:text-white transition-all duration-300 tracking-wide"
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
