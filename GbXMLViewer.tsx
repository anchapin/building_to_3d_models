import React from 'react';

export default function GbXMLViewer({ xmlContent }) {
  // Format XML with syntax highlighting
  const formatXML = (xml) => {
    if (!xml) return '';
    
    // Replace < and > with &lt; and &gt; to prevent HTML rendering
    let formattedXml = xml
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;');
    
    // Add syntax highlighting classes
    formattedXml = formattedXml
      // Tags
      .replace(/&lt;(\/?[a-zA-Z0-9_:-]+)(?=\s|&gt;)/g, '<span class="text-blue-500">&lt;$1</span>')
      // Attributes
      .replace(/\s([a-zA-Z0-9_:-]+)="([^"]*)"/g, ' <span class="text-yellow-600">$1</span>=<span class="text-green-500">"$2"</span>');
    
    return formattedXml;
  };

  return (
    <div className="w-full">
      <div className="bg-gray-800 text-white rounded-lg p-4 h-96 overflow-auto font-mono text-sm">
        {xmlContent ? (
          <pre dangerouslySetInnerHTML={{ __html: formatXML(xmlContent) }} />
        ) : (
          <div className="flex items-center justify-center h-full text-gray-400">
            No gbXML content to display
          </div>
        )}
      </div>
      
      <div className="mt-4 flex space-x-4">
        <button className="bg-green-600 hover:bg-green-700 text-white font-bold py-2 px-4 rounded">
          Download gbXML
        </button>
        <button className="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded">
          Validate gbXML
        </button>
        <button className="bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-4 rounded">
          Copy to Clipboard
        </button>
      </div>
    </div>
  );
}
