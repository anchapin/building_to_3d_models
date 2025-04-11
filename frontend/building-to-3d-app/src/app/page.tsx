import Link from 'next/link';

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <div className="z-10 max-w-5xl w-full items-center justify-center font-mono text-sm">
        <h1 className="text-4xl font-bold mb-8 text-center">
          Building to 3D Models
        </h1>
        
        <p className="text-lg mb-8 text-center">
          Convert building plans and elevations to 3D models for energy analysis
        </p>
        
        <div className="flex justify-center">
          <Link 
            href="/upload" 
            className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
          >
            Get Started
          </Link>
        </div>
        
        <div className="mt-16 grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="border p-6 rounded-lg">
            <h2 className="text-xl font-bold mb-4">Upload Plans</h2>
            <p>Upload your floor plans and elevation drawings to get started.</p>
          </div>
          
          <div className="border p-6 rounded-lg">
            <h2 className="text-xl font-bold mb-4">Set Scale</h2>
            <p>Define the scale to ensure accurate measurements in your 3D model.</p>
          </div>
          
          <div className="border p-6 rounded-lg">
            <h2 className="text-xl font-bold mb-4">Generate 3D Model</h2>
            <p>Create a 3D model and export to gbXML for energy analysis.</p>
          </div>
        </div>
      </div>
    </main>
  );
}
