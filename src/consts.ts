export const SITE = {
  url: 'https://datawise.dev',
  name: 'Datawise',
  title: 'Datawise — SQL, BigQuery & Python for Data Engineers',
  description:
    'Practical SQL, BigQuery, and Python tutorials for data engineers. Real-world case studies, no fluff — written by a Staff Data Engineer with 12+ years in the field.',
  logo: '/logo.png',
  newsletter: { name: 'Not just SQL', url: 'https://www.notjustsql.com' },
};

export const AUTHOR = {
  name: 'Constantin Lungu',
  bio: 'Senior Data Engineer • Contractor / Freelancer • GCP & AWS Certified',
  url: 'https://cnstlungu.com/',
  photo: '/images/author.jpg',
  links: {
    LinkedIn: 'https://www.linkedin.com/in/constantin-lungu-668b8756/',
    GitHub: 'https://github.com/cnstlungu',
  },
};

// Same order as the Hashnode navbar.
export const NAV = [
  { label: 'Practical SQL', href: '/series/practical-sql' },
  { label: 'Python for Data Engineers', href: '/series/python' },
  { label: 'My Data Journey', href: '/series/my-data-journey' },
  { label: 'Data Ops', href: '/series/data-ops' },
  { label: 'Archive', href: '/archive' },
];
