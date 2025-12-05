import { NextRequest, NextResponse } from 'next/server';

export async function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams;
  const amazonURL = searchParams.get('url');

  if (!amazonURL) {
    return NextResponse.json(
      { success: false, message: 'Amazon URL is required' },
      { status: 400 }
    );
  }

  try {
    const res = await fetch(amazonURL, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:145.0) Gecko/20100101 Firefox/145.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Alt-Used': 'www.amazon.in',
        'Connection': 'close'
      },
    });

    if (!res.ok) {
      console.log("Live price fetch failed with status:", res.status);
      return NextResponse.json(
        { success: false, message: `Failed to fetch: ${res.status}` },
        { status: res.status }
      );
    }

    const html = await res.text();

    // Parse HTML to get the price from span with class="a-price-whole"
    const spanRegex = /<span[^>]*class="[^"]*a-price-whole[^"]*"[^>]*>([^<]+)<\/span>/i;
    const match = html.match(spanRegex);

    if (match && match[1]) {
      // remove commas & whitespace
      const cleanPrice = match[1].replace(/,/g, '').trim();
      console.log("Live price found:", cleanPrice);
      return NextResponse.json({
        success: true,
        price: cleanPrice
      });
    }

    console.log("Could not find price in Amazon page HTML");
    return NextResponse.json(
      { success: false, message: 'Could not find price in Amazon page HTML' },
      { status: 404 }
    );

  } catch (error) {
    console.error("Error fetching live price:", error);
    return NextResponse.json(
      { success: false, message: `Error fetching live price: ${error instanceof Error ? error.message : 'Unknown error'}` },
      { status: 500 }
    );
  }
}

