import Link from 'next/link';

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-8">
      <div className="z-10 w-full max-w-5xl items-center justify-between font-mono text-sm">
        <h1 className="text-4xl font-bold text-center mb-8">Building-to-3D Conversion</h1>
        
        <div className="bg-white p-6 rounded-lg shadow-md mb-8">
          <h2 className="text-2xl font-semibold mb-4">Convert Building Plans to 3D Models</h2>
          <p className="mb-4">
            Upload building elevation images and floor plans to generate a 3D model suitable for building energy modeling.
            The application will process your images, detect architectural elements, and generate a gbXML file.
          </p>
          <div className="flex justify-center">
            <Link 
              href="/upload" 
              className="bg-green-600 hover:bg-green-700 text-white font-bold py-2 px-4 rounded"
            >
              Start New Project
            </Link>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white p-4 rounded-lg shadow">
            <h3 className="text-xl font-semibold mb-2">1. Upload Images</h3>
            <p>Upload building elevation images (minimum 4) and floor plans (one per level).</p>
          </div>
          <div className="bg-white p-4 rounded-lg shadow">
            <h3 className="text-xl font-semibold mb-2">2. Set Scale</h3>
            <p>Indicate scale on each image to convert from pixels to real-world measurements.</p>
          </div>
          <div className="bg-white p-4 rounded-lg shadow">
            <h3 className="text-xl font-semibold mb-2">3. Generate 3D Model</h3>
            <p>Process images to create a 3D model and export to gbXML format.</p>
          </div>
        </div>

        <div className="bg-gray-100 p-6 rounded-lg">
          <h2 className="text-2xl font-semibold mb-4">How It Works</h2>
          <ol className="list-decimal pl-6 space-y-2">
            <li>Our system detects edges and features in your building plans</li>
            <li>Elevation views are combined with floor plans to create a 3D model</li>
            <li>The 3D model is converted to gbXML format for energy modeling</li>
            <li>You can download the gbXML file for use in energy modeling software</li>
          </ol>
        </div>
      </div>
    </main>
  );
}
