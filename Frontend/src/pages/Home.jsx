import React from 'react'
import Navbar from '../components/Navbar'
import HeroSection from '../components/HeroSection'
import VideoSection from '../components/VideoSection'
import Project from '../components/Project'
import Form from '../components/Form'

const Home = () => {
  return (
    <div>
      <Navbar/>
      <HeroSection/>
      <VideoSection/>
      <Project/>
      <Form/>
    </div>
  )
}

export default Home
