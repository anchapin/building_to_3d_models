import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'Building to 3D Models',
  description: 'Convert building plans to 3D models for energy analysis',
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>
        <header className="bg-gray-800 text-white p-4">
          <div className="container mx-auto">
            <h1 className="text-xl font-bold">Building to 3D Models</h1>
          </div>
        </header>
        {children}
        <footer className="bg-gray-800 text-white p-4 mt-auto">
          <div className="container mx-auto text-center">
            <p>© 2023 Building to 3D Models</p>
          </div>
        </footer>
      </body>
    </html>
  );
}
